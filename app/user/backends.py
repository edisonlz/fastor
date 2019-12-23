#coding=utf-8

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# from app.user.lib.ldapauth import validate_user
# from app.user.lib.ldapauth2 import validate_user, ServerIsBusy
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

# import logging
# logger = logging.getLogger()
# formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
# file_handler = logging.FileHandler("/tmp/rdm.log")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


class LDAPBackend(ModelBackend):

    """
    Authenticates for LDAP
    """
    def authenticate(self, username=None, password=None, **kwargs):

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except Exception:
            raise u"未注册用户, 请申请账户"
        else:
            username = username.split('@')[0]
            
            try:
                is_valid = 1
            except:
                raise u"邮件服务器忙，请稍后再试"
            else:
                if is_valid:
                    user.set_password(password)
                    user.save()
                    return user
                else:
                    raise u"邮箱密码错误"