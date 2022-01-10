from .common import *

DEBUG = False



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'site_p', # DB명
        'USER': 'sbsstlocal', # DBMS 접속 아이디
        'PASSWORD': '1234', # DBMS 접속 비번
        'HOST': '172.17.0.1', # DBMS 주소
        'PORT': '3306', # DBMS 포트
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

