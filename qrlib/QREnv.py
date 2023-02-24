from robot.libraries.BuiltIn import BuiltIn
import os


class QREnv:

    
    PLATFORM_VERSION = 2
    
    NO_PLATFORM = True
    
    # IDENTIFIER = BuiltIn().get_variable_value("${identifier}")        # For platform v1
    # IDENTIFIER = os.environ.get("identifier")                         # For platform v2
    IDENTIFIER = "f2a2e5ee-5fcf-47ac-9ab0-9870647a225f"                 # For testing on server via localhost
    
    VERIFY_SSL = False
    DEBUG = True
    
    BASE_DIR = os.environ.get("ROBOT_ROOT")
    ARTIFACT_DIR = os.environ.get("ROBOT_ARTIFACTS")
    DEFAULT_STORAGE_LOCATION = os.path.join(BASE_DIR, 'storage_downloads')

    # ENVIRONMENTS
    ENV_LOCAL = "LOCAL"
    ENV_QR_DEV = "QR_DEV"
    ENV_QR_UAT = "QR_UAT"
    ENV_UAT = "UAT"
    ENV_PRODUCTION = "PRODUCTION"

    # URLS
    URL_LOCAL = "http://127.0.0.1:8000/api/v1"
    URL_QR_DEV_URL = "http://13.58.117.7:8000/api/v1"
    URL_QR_UAT_URL = "http://13.58.117.7:8000/api/v1"
    URL_UAT_URL = "http://18.217.209.236/api/v1"
    URL_PROD = ""

    ENV_URL = {
        ENV_LOCAL: URL_LOCAL,
        ENV_QR_DEV: URL_QR_DEV_URL,
        ENV_QR_UAT: URL_QR_UAT_URL,
        ENV_UAT: URL_UAT_URL,
        ENV_PRODUCTION: URL_PROD
    }

    # ENVIRONMENT = os.environ.get("ENVIRONMENT")
    ENVIRONMENT = ENV_UAT
    
    try:
        BASE_URL = ENV_URL[ENVIRONMENT]
    except Exception as e:
        BASE_URL = URL_LOCAL


    QUEUE_NAMES = []
    STORAGE_NAMES = []
    VAULT_NAMES = []

    QUEUES = {}
    STORAGES = {}
    VAULTS = {}
    
