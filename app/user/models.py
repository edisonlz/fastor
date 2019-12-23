# coding=utf-8
import functools
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        (0, "管理员"),
        (1, "普通用户"),
        (2, "运营"),
    )

    NORMAL = 1
    EDITOR = 2
    SUPERUSER = 0

    STATUS_DELETE = 2
    STATUS_NORMAL = 0


    status = models.IntegerField(verbose_name='状态', default=0)
    role = models.IntegerField(verbose_name=u'用户角色', choices=ROLE_CHOICES, default=1)

    class Meta:
        app_label = 'user'

    @property
    def role_name(self):
        role_dic = dict(self.ROLE_CHOICES)
        return role_dic.get(self.role, "无")

    @property
    def is_manager(self):
        return self.is_super or self.is_super_editor

    