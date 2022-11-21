from robot.libraries.BuiltIn import BuiltIn
import os

class QREnv:

    IDENTIFIER = BuiltIn().get_variable_value("${identifier}") # Get from env variable later
    VERIFY_SSL = False
    TEST_SETUP_ONLY = False
    DEBUG = True
    NO_PLATFORM = True
    BASE_DIR = os.environ.get("ROBOT_ROOT")
    ARTIFACT_DIR = os.environ.get("ROBOT_ARTIFACTS")

    # ENVIRONMENTS
    ENV_LOCAL = "LOCAL"
    ENV_QR_DEV = "QR_DEV"
    ENV_QR_UAT = "QR_UAT"
    ENV_CLIENT_UAT = "UAT"
    ENV_PRODUCTION = "PRODUCTION"

    # URLS
    LOCAL_URL = "http://localhost:8000/api/v1"
    QR_DEV_URL = "http://13.58.117.7:8000/api/v1"
    QR_UAT_URL = "http://13.58.117.7:8000/api/v1"
    CLIENT_UAT_URL = "http://10.0.16.90:8000/api/v1"
    PROD_URL = "http://10.0.16.68/api/v1"

    ENV_URL = {
        ENV_LOCAL: LOCAL_URL,
        ENV_QR_DEV: QR_DEV_URL,
        ENV_QR_UAT: QR_UAT_URL,
        ENV_CLIENT_UAT: CLIENT_UAT_URL,
        ENV_PRODUCTION: PROD_URL
    }

    # ENVIRONMENT = os.environ.get("ENVIRONMENT")
    ENVIRONMENT = ENV_PRODUCTION
    try:
        BASE_URL = ENV_URL[ENVIRONMENT]
    except Exception as e:
        BASE_URL = LOCAL_URL

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
    VAULT_NAMES = ['test','test1']

    QUEUES = {}
    STORAGES = {}
    VAULTS = {}
