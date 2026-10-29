import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_token3")
BOT_TOKEN2 = os.getenv("BOT_token2")
BOT_TOKEN3 = os.getenv("BOT_token1")

CyndykShopAPI_key = os.getenv("CyndykShopAPI_key")
NintendoAccountManager_login = os.getenv("NintendoAccountManager_login")
NintendoAccountManager_password = os.getenv("NintendoAccountManager_password")
MAIL_API_KEY = os.getenv("MAIL_API_KEY")
AMS_APP_SECRET = os.getenv("AMS_APP_SECRET")


MAIL_API_BASE_URL = "https://mail-aggregator.cyndykshop.su"
MAIL_API_TIMEOUT = 30  





AEGIS_API_KEY = os.getenv("AEGIS_API_KEY")



GOOGLE_TOKEN = 'keys/cyndyk71-2c2122475ee2.json'
GOOGLE_REAL_TOKEN = "keys/token.json"
GOOGLE_CREDS = "keys/credentials.json"

ADMIN_DATA_SHELVE = "data/admin-data"
BOT_END_DATA_SHELVE = "data/bot_end_data"
BOT_END_DATA_RESERV_SHELVE = "data/bot_end_data_reserv"
DEL_ACCS_DATA_SHELVE = "data/del_accs"
AU_CODE_HAND_DATA_SHELVE = 'data/au_code_hand'
MAX_PLEASE_DATA_SHELVE = 'data/max_please'
AU_CODE_DATA_SHELVE = "data/au_code"



DANCEDANCE_VIDEO = "video/breakdance-break.mp4"