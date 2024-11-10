
import os

class Config:
    API_ID = 25951341#os.environ.get("API_ID", "21714374")
    API_HASH = "f1f620f451989a04994e1d0796466d55"#os.environ.get("API_HASH", "700092e37d7da9a7b781994b7503a488")
    BOT_TOKEN = "6674516595:AAGXTP1vxs5TI4zR-Twhq739rU7U-roDmgQ"#os.environ.get("BOT_TOKEN", "") 
    BOT_SESSION = "forward-bot"#os.environ.get("BOT_SESSION", "forward-bot") 
    DB_URL = "mongodb+srv://admin:asd1234@clouster0.b2fgx.mongodb.net/?retryWrites=true&w=majority&appName=Clouster0"#os.environ.get("DB_URL", "")
    DB_NAME = "User_bot"#os.environ.get("DB_NAME", "madflixbotz")
    OWNER_ID = 971580959#[int(id) for id in os.environ.get("OWNER_ID", '6140468904').split()]
    CHANNEL_ID = -1002422039132

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []

