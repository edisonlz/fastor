# coding=utf-8
from django.db import models
from wi_cache import function_cache
from django.conf import settings
from app.iclass.utils.short_id import ShortID


class Editor(models.Model):
    """
    编辑内容转URL
    """

    STATUS_NORMAL = 0
    STATUS_CLOSE = 1

    title = models.CharField(max_length=255, verbose_name=u'标题', default='')
    content = models.TextField(verbose_name=u'内容')

    status = models.IntegerField(verbose_name=u'状态', default=1, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', db_index=True)


    class Meta:
        app_label = "iclass"

    def to_json(self):
        r = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return r

    @property
    def status_ch(self):
        if self.status == self.STATUS_NORMAL:
            return '开启'
        else:
            return '关闭'

    @classmethod
    def get_editor(cls, _id):
        return Editor.objects.filter(id=_id).first()

    @property
    def short_id(self):
        return ShortID().toHex(self.id)

    @property
    def short_url(self):
        return "%s/e/%s" % (settings.HOST, self.short_id)


