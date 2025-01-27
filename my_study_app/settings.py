from .settings_common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')  # 環境変数から読み込む

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]  # 許可するホスト名リスト

STATIC_ROOT = '/usr/share/nginx/html/static'  # 静的ファイルの保存場所
MEDIA_ROOT = '/usr/share/nginx/html/media'

# Amazon SES関連の設定
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'accounts': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'ai_support': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'analytics': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'ascension': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'learning': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'learning_test': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D', # ログローテーション間隔の単位
            'interval': 1,
            'backupCount': 7, 
        },  
    },
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levalname)s]',
                '%(pathname)s(Line:%(lineno)d),'
                '%(message)s',
            ])
        },
    }
}