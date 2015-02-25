import logging
import urllib.request, base64
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from urllib.parse import urlparse, urlencode, quote_plus
from hashlib import sha1, md5
from hmac import new as hmac
import json

import requests
from pprint import pprint
import binascii


class VuforiaBaseError(Exception):
    def __init__(self, exc, response):
        self.transaction_id = response['transaction_id']
        self.result_code = response['result_code']
        self.exc = exc

class VuforiaRequestQuotaReached(VuforiaBaseError):
    pass

class VuforiaAuthenticationFailure(VuforiaBaseError):
    pass

class VuforiaRequestTimeTooSkewed(VuforiaBaseError):
    pass

class VuforiaTargetNameExist(VuforiaBaseError):
    pass

class VuforiaUnknownTarget(VuforiaBaseError):
    pass

class VuforiaBadImage(VuforiaBaseError):
    pass

class VuforiaImageTooLarge(VuforiaBaseError):
    pass

class VuforiaMetadataTooLarge(VuforiaBaseError):
    pass

class VuforiaDateRangeError(VuforiaBaseError):
    pass

class VuforiaFail(VuforiaBaseError):
    pass


class Vuforia(object):
    def __init__(self, access_key, secret_key,
                 host="https://vws.vuforia.com"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = host

    def _send(self, url, method, data=None, headers=None, type=None):
        """
        method handler of requests
        """
        try:
            if method == 'POST':
                return requests.post(url=url, headers=headers, data=data)
            elif method == 'GET':
                return requests.get(url=url, headers=headers, data=data)
            elif method == 'PUT':
                return requests.put(url=url, headers=headers, data=data)
            elif method == 'DELETE':
                return requests.delete(url=url, headers=headers, data=data)
        except requests.exceptions.ConnectionError:
            return None

    def _get_rfc1123_date(self):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)

    def _get_request_path(self, req):
        #o = urlparse(req.get_full_url())
        o = urlparse(req.url)
        return o.path

    def _hmac_sha1_base64(self, key, message):
        # On python3, HMAC needs bytes for key and msg.
        return base64.b64encode(
                    hmac(key.encode(),
                         message.encode(),
                         sha1).digest()).decode()

    def _get_content_md5(self, req):
        if req.data:

            #print("hexdigenst: ", md5(req.data.encode()).hexdigest())
            #print("hexdigenst(ascii): ",
            #      md5(req.data.encode('ascii')).hexdigest())

            return md5(req.data.encode()).hexdigest()
        return "d41d8cd98f00b204e9800998ecf8427e"

    def _get_content_type(self, req):
        if req.method in ["POST", "PUT"]:
            return "application/json"
        return ""

    def _get_authenticated_response(self, req):
        rfc1123_date = self._get_rfc1123_date()
        string_to_sign =\
            req.method + "\n" +\
            self._get_content_md5(req) + "\n" +\
            self._get_content_type(req) + "\n" +\
            rfc1123_date + "\n" +\
            self._get_request_path(req)

        #print("string_to_sign: ", string_to_sign)
        #print("rfc1123_date: ", rfc1123_date)

        signature = self._hmac_sha1_base64(self.secret_key, string_to_sign)

        #print(type(signature))
        #print("signature: ", signature)

        req.headers['Date'] =  rfc1123_date
        auth_header = 'VWS %s:%s' % (self.access_key, signature)
        req.headers['Authorization'] = auth_header
        try:

            #p = req.prepare()

            #print(req.url)
            #print("Request.prepare().path_url: ", p.path_url)
            #print(type(req.data))
            #print(req.data)
            #print(req.headers)

            if not req.data:
                data_to_send = None
            else:
                data_to_send = req.data.encode()

            #return requests.Session().send(p)
            #return requests.post(req.url, data=req.data.encode(),
            #                     headers=req.headers)
            return self._send(req.url, req.method, data=data_to_send,
                              headers=req.headers)

        except requests.exceptions.HTTPError as e:
            print("ERROR: ", e)
            response = json.loads(e.read().decode('utf-8'))

            result_code = response['result_code']
            if result_code == 'RequestTimeTooSkewed':
                raise VuforiaRequestTimeTooSkewed(e, response)
            elif result_code == 'TargetNameExist':
                raise VuforiaTargetNameExist(e, response)
            elif result_code == 'RequestQuotaReached':
                raise VuforiaRequestQuotaReached(e, response)
            elif result_code == 'UnknownTarget':
                raise VuforiaUnknownTarget(e, response)
            elif result_code == 'BadImage':
                raise VuforiaBadImage(e, response)
            elif result_code == 'ImageTooLarge':
                raise VuforiaImageTooLarge(e, response)
            elif result_code == 'MetadataTooLarge':
                raise VuforiaMetadataTooLarge(e, response)
            elif result_code == 'DateRangeError':
                raise VuforiaDateRangeError(e, response)
            elif result_code == 'Fail':
                raise VuforiaFail(e, response)
            else:
                logging.error("Couldn't process %s response from Vuforia" % response)

            raise e  # re-raise the initial exception if can't handle it

    def get_target_by_id(self, target_id):
        url = '%s/targets/%s' % (self.host, target_id)
        req = requests.Request(method='GET', url=url)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())['target_record']

    def get_target_ids(self):
        url = '%s/targets' % self.host
        req = requests.Request(method='GET', url=url)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())['results']

    def get_summary(self):
        url = '%s/summary' % self.host
        req = requests.Request(method='GET', url=url)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())

    def get_targets(self):
        targets = []
        for target_id in self.get_target_ids():
            targets.append(self.get_target_by_id(target_id))
        return targets

    def add_target(self, data):
        url = '%s/targets' % self.host
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        req = requests.Request(method='POST', url=url, data=data,
                               headers=headers)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())

    def update_target(self, target_id, data):
        # Takes time to process
        url = '%s/targets/%s' % (self.host, target_id)
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        req = requests.Request(method='PUT', url=url, data=data,
                               headers=headers)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())

    def delete_target(self, target_id):
        # Takes time to process
        url = '%s/targets/%s' % (self.host, target_id)
        req = requests.Request(method='DELETE', url=url)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())

    def check_duplicates(self, target_id):
        url = '%s/duplicates/%s' % (self.host, target_id)
        req = requests.Request(method='GET', url=url)
        response = self._get_authenticated_response(req)
        return json.loads(response.content.decode())

def main():
    v = Vuforia(access_key="44fb7f9c4ce4d05cddd29a79ed2cb41d56463a3f",
                secret_key="5993b47b9ae0912e10ece2c98f59219867a01e42")

    for target in v.get_targets():
        print("TARGET: ")
        pprint(target)
        print("DUPLICATES: ")
        pprint(v.check_duplicates(target['target_id']))

    #image_file = open('/Users/js/Desktop/tiger.jpg', "rb")
    # Python3では byte型になってしまうので、decode()する。
    #image = base64.b64encode(image_file.read()).decode('utf-8')
    #print("image: ", type(image))      # Python2

    #metadata_file = open('/Users/js/Desktop/vuforia_python/meta.txt', "rb")
    #metadata = base64.b64encode(metadata_file.read())

    # Caution: the type of width key is number instead of string.
    #pprint(v.add_target(
    #    {"name": "tiger2", "width": 320, "image": image, "active_flag": 1}))


    #pprint(v.delete_target("866cf0dcd1444123a3da3348acd6d00b"))

    print("SUMMARY: ")
    pprint(v.get_summary())
    #pprint(v.update_target("43d88019ad64469c8e63e3bcb958a1d2",
    #                       {"name": "tiger1"}))

if __name__ == "__main__":
    main()
