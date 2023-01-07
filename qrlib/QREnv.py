from robot.libraries.BuiltIn import BuiltIn
import os


class QREnv:

    # IDENTIFIER = BuiltIn().get_variable_value("${identifier}") # Get from env variable later
    IDENTIFIER = "3926d8d3-0731-41d5-a156-17e26d9f8cfb"
    VERIFY_SSL = False
    TEST_SETUP_ONLY = False
    DEBUG = True
    NO_PLATFORM = True
    PLATFORM_VERSION = 1

    BASE_DIR = os.environ.get("ROBOT_ROOT")
    ARTIFACT_DIR = os.environ.get("ROBOT_ARTIFACTS")

    # ENVIRONMENTS
    ENV_LOCAL = "LOCAL"
    ENV_QR_DEV = "QR_DEV"
    ENV_QR_UAT = "QR_UAT"
    ENV_UAT = "UAT"
    ENV_PRODUCTION = "PRODUCTION"

    # URLS
    URL_LOCAL = "http://127.0.0.1:8000/api/v1/"
    URL_QR_DEV_URL = "http://13.58.117.7:8000/api/v1/"
    URL_QR_UAT_URL = "http://13.58.117.7:8000/api/v1/"
    URL_UAT_URL = ""
    URL_PROD = ""

    ENV_URL = {
        ENV_LOCAL: URL_LOCAL,
        ENV_QR_DEV: URL_QR_DEV_URL,
        ENV_QR_UAT: URL_QR_UAT_URL,
        ENV_UAT: URL_UAT_URL,
        ENV_PRODUCTION: URL_PROD
    }

    # ENVIRONMENT = os.environ.get("ENVIRONMENT")
    ENVIRONMENT = ENV_LOCAL
    
    try:
        BASE_URL = ENV_URL[ENVIRONMENT]
    except Exception as e:
        BASE_URL = URL_LOCAL

    # SMTP Settings
    SMTP_SERVER = ""
    SMTP_PORT = ""
    SMTP_ACCOUNT = ""
    SMTP_PASSWORD = ""
    SMTP_USE_TLS = True
    SMTP_VERIFY_SSL = False

    BOT_NAME = 'TEST'
    HEADLESS = False
    SELENIUM_SPEED = None
    TIMEOUT = 30
    CONSECUTIVE_ERROR_RETRY = 3

    QUEUE_NAMES = ['test']
    STORAGE_NAMES = ['test']
    VAULT_NAMES = ['test', 'test1']

    QUEUES = {}
    STORAGES = {''}
    VAULTS = {}

    # * Storage Buckets, Do not change this settings
    STORAGE_LOCAL = 'local'
    STORAGE_S3 = 's3'
    DEFAULT_STORAGE_LOCATION = os.path.join(os.getcwd(), 'downloads')
