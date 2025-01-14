from .settings_common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n($bsn(07p#u6e5^wd#&uyi8yd#^!&%ef!izlftmkykeyh!cqz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガー設定
    'loggers': {
        # Djangoが利用
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },

        # diaryアプリケーションが利用
        'diary': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
    # ハンドラ設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev',
        },
    },
    # フォーマッタ設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
