from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
                                       BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone

import hashlib
import os.path
from datetime import datetime, date

# カスタムUserモデルを定義する場合はこれも必要
class UserProfileManager(BaseUserManager):
    def create_user(self, acc_type_id, parent_admin_id, parent_agency_id,
                    enterprise, person, address, email, phone_number,
                    password=None):
        # Django ドキュメントのサンプルを参考に。
        if not acc_type_id:
            raise ValueError('Users must have an account type ID')

        user = self.model(acc_type_id=acc_type_id,
                          parent_admin_id=parent_admin_id,
                          parent_agency_id=parent_agency_id,
                          enterprise=enterprise, person=person,
                          address=address, email=email,
                          phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, acc_type_id, password):
        user = self.create_user(acc_type_id=acc_type_id,
                                parent_admin_id=parent_admin_id,
                                parent_agency_id=parent_agency_id,
                                enterprise=enterprise, person=person,
                                address=address, email=email,
                                phone_number=phone_number,
                                password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
        unique_together = ('acc_type_id', 'user_id')
        permissions = (
            ('running', 'can log in'),
        )

    ACC_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Agency'),
        (3, 'Company')
    )

    # Attributes
    identifier = models.CharField('アカウントID', max_length=11,
                                  unique=True)
    user_id     = models.IntegerField('ユーザーID', null=True)
    acc_type_id = models.SmallIntegerField('アカウントタイプID',
                                           choices=ACC_TYPE_CHOICES)
    # substitute password of User for this
    #pw          = models.CharField('ログインパスワード', max_length=10)
    parent_admin_id     = models.IntegerField('親AdminID', default=1)
    parent_agency_id    = models.IntegerField('親AgencyID', null=True)
    user_running    = models.SmallIntegerField('稼働フラグ', default=0)
    enterprise      = models.CharField('企業名', max_length=64)
    person          = models.CharField('担当者名', max_length=64)
    address         = models.CharField('住所', max_length=64)
    email           = models.EmailField('メールアドレス', )
    phone_number    = models.CharField('電話番号', max_length=16,
            error_messages={
              'incomplete': '数字もしくはハイフンのみで入力してください。'},
            validators=[RegexValidator(r'^[\d-]+$',
                          '数字もしくはハイフンのみで入力してください。')])
    created_at  = models.DateTimeField('作成日', default=timezone.now,
                                       editable=False)
    updated_at  = models.DateTimeField('更新日', editable=False, null=True)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['acc_type_id', 'enterprise', 'email']

    objects = UserProfileManager()

    def __str__(self):
        return self.identifier

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_active(self):
        return True

    def save(self, *args, **kwargs):
        self.updated_at = date.today()
        if self.id: # アップデートの場合
            super(UserProfile, self).save()
        else:       # 新規登録の場合は、関連モデルも登録する。
            if self.acc_type_id == 1:
                user = AdminUser()
                ACC_TYPE_PREFIX = 'ad-'
            elif self.acc_type_id == 2:
                user = AgencyUser()
                ACC_TYPE_PREFIX = 'ag-'
            elif self.acc_type_id == 3:
                user = CompanyUser()
                ACC_TYPE_PREFIX = 'co-'
            user.save()
            self.user_id = user.id
            self.identifier = ACC_TYPE_PREFIX + str(self.user_id).zfill(8)
            super(UserProfile, self).save()
            user.user_profile_id=self.id
            user.save()

    def delete(self, **kwargs):
        if self.acc_type_id == 1:
            user = AdminUser.objects.get(id=self.user_id)
        elif self.acc_type_id == 2:
            user = AgencyUser.objects.get(id=self.user_id)
        elif self.acc_type_id == 3:
            user = CompanyUser.objects.get(id=self.user_id)
        user.delete()
        super(UserProfile, self).delete()


# 各ユーザー種別でIDをインクリメントするために別テーブルを作る。
# idアトリビュートがそのIDに当たり、
# user_profile_idアトリビュートが、対応するUserProfileのIDに当たる。
class AdminUser(models.Model):
    # ForeignKeyだと、UserProfile.save()のオーバーライドがしにくかった。
    #user_profile = models.ForeignKey(UserProfile, verbose_name="Admin")
    user_profile_id = models.IntegerField("AdminID", unique=True, null=True)
    def __str__(self):
        return str(self.id)

class AgencyUser(models.Model):
    user_profile_id = models.IntegerField("AgencyID",
                                          unique=True, null=True)
    def __str__(self):
        return str(self.id)

class CompanyUser(models.Model):
    user_profile_id = models.IntegerField("CompanyID",
                                          unique=True, null=True)
    def __str__(self):
        return str(self.id)


class Content(models.Model):
    class Meta:
        verbose_name = 'コンテンツ'
        verbose_name_plural = 'コンテンツ'


    def get_image_path(instance, filename):
        return "images/%s%s" % (instance.contract_no,
                                os.path.splitext(filename)[1])

    # Attributes
    contract_no     = models.AutoField('契約番号', primary_key=True)
    #contract_no     = models.PositiveIntegerField('契約番号',
    #                                              primary_key=True)
    image           = models.ImageField('マーカー',
                                        upload_to =get_image_path, null=True,
                                        blank=True)
    title           = models.CharField('タイトル', max_length=64, null=True)
    target_id       = models.CharField('ターゲットID', max_length=128,
                                       null=True)
    mapping_url     = models.URLField('マッピングURL', max_length=128,
                                       null=True)
    open_from       = models.DateField('公開期間 自', default=timezone.now)
    open_to         = models.DateField('公開期間 至', null=True, blank=True)
    is_open         = models.SmallIntegerField('公開フラグ', default=0)
    sort            = models.IntegerField('ソートインデックス', default=0)

    company         = models.ForeignKey(UserProfile, verbose_name="Company",
                                        null=True)

    recognition     = models.SmallIntegerField('認識率', default=0,
                                               null=True)
    delete_flag     = models.SmallIntegerField('論理削除', default=0)
    check_duplicate = models.SmallIntegerField('重複チェック', default=0)
    contracted_at   = models.DateField('契約日', default=timezone.now)
    terminated_at   = models.DateField('契約解除日', null=True)
