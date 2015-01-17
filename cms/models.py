from django.db import models
from datetime import datetime, date
from django.utils import timezone

class CmsUser(models.Model):
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
        unique_together = ('acc_type_id', 'user_id')

    ACC_TYPE_CHOICES = (
        (0, 'Admin'),
        (1, 'Agency'),
        (2, 'Company')
    )

    # Attributes
    user_id     = models.IntegerField('ユーザーID', )
    acc_type_id = models.CharField('アカウントタイプID', max_length=2,
                                   choices=ACC_TYPE_CHOICES)
    pw          = models.CharField('ログインパスワード', max_length=10)
    parent_admin_id     = models.IntegerField('親AdminID', default=0)
    parent_agency_id    = models.IntegerField('親AgencyID', default=0)
    user_running    = models.SmallIntegerField('稼働フラグ', default=0)
    enterprise      = models.CharField('企業名', max_length=64)
    person          = models.CharField('担当者名', max_length=64)
    address         = models.CharField('住所', max_length=64)
    mail_address    = models.EmailField('メールアドレス', )
    phone_number    = models.CharField('電話番号', max_length=16)
    created_at  = models.DateTimeField('作成日', default=datetime.today(),
                                       editable=False)
    updated_at  = models.DateTimeField('更新日', editable=False)


class Content(models.Model):
    class Meta:
        verbose_name = 'コンテンツ'
        verbose_name_plural = 'コンテンツ'

    # Attributes
    contract_no     = models.PositiveIntegerField('契約番号',
                                                  primary_key=True)
    title           = models.CharField('タイトル', max_length=64)
    target_id       = models.CharField('ターゲットID', max_length=128)
    mapping_url     = models.CharField('マッピングURL', max_length=128)
    open_from       = models.CharField('公開期間 自', max_length=16)
    open_to         = models.CharField('公開期間 至', max_length=16,
                                       null=True)
    is_open         = models.SmallIntegerField('公開フラグ', default=0)
    sort            = models.IntegerField('ソートインデックス', default=0)
    user_id         = models.IntegerField('CompanyID')
    recognition     = models.SmallIntegerField('認識率', default=0)
    contracted_at   = models.CharField('契約日', max_length=16)
    delete_flag     = models.SmallIntegerField('論理削除', default=0)
    check_duplicate = models.SmallIntegerField('重複チェック', default=0)
    terminated_at   = models.CharField('契約解除日', max_length=16,
                                       default="")
