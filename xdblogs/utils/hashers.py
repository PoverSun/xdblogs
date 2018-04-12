# -*- coding: utf-8 -*-
import hashlib
import hashlib
from local_config import PASSWORD_SALT

# 加密和检查密码
# raw_password 原始密码
# salt 盐
def make_password(raw_password,email,salt=None):
    if not salt:
        salt = PASSWORD_SALT
    if not raw_password:
        return False
    hash_password = hashlib.md5(raw_password+email+salt).hexdigest()

    return hash_password


def check_password(raw_password,password,email):
    if not raw_password:
        return False

    temp_password = make_password(raw_password,email)
    if temp_password == password:
        return True
    else:
        return False
