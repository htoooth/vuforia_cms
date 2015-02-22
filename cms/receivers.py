from django.dispatch import receiver
from django.dispatch import receiver
from django.db.models.signals import post_save

from cms.models import Content
from vuforia_cms import settings

import os
from PIL import Image

def create_thumbnail(content_instance, size):
    if content_instance.image:
        origin_path = content_instance.image.path
        new_path = os.path.join(settings.MEDIA_ROOT, 'images' + str(size),
                       str(content_instance.contract_no) + os.path.splitext(
                                            content_instance.image.name)[1])
        # 画像ファイルを readモードで読み込み。
        img = Image.open(origin_path, 'r')
        # resizeではなくthumbnailを利用して縮小。上書きに注意。
        img.thumbnail((size, size), Image.ANTIALIAS)
        # リサイズ後の画像を保存。
        img.save(new_path, quality=100, optimize=True)

@receiver(post_save, sender=Content)
def create_thumbnail_post_save(sender, instance, **kwargs):
    create_thumbnail(instance, 100)
    create_thumbnail(instance, 500)





