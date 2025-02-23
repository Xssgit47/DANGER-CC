from pyrogram import Client 
import json
from FUNC.server_stats import *

plugins = dict(root="7595971863:AAEpBqA2OGRMxxXLpNsQmhAxuVEnW464AhQ")

with open("FILES/config.json", "r", encoding="utf-8") as f:
    DATA      = json.load(f)
    API_ID    = DATA["23418117"]
    API_HASH  = DATA["e93479e4b3eae090bf90a978b14ffc09"]
    BOT_TOKEN = DATA["7595971863:AAEpBqA2OGRMxxXLpNsQmhAxuVEnW464AhQ"]

user = Client( 
            "Scrapper", 
             api_id   = API_ID, 
             api_hash = API_HASH
              )

bot = Client(
    "MY_BOT", 
    api_id    = API_ID, 
    api_hash  = API_HASH, 
    bot_token = BOT_TOKEN, 
    plugins   = plugins 
)



if __name__ == "__main__":
    # send_server_alert()
    print("Done Bot Active ✅")
    print("NOW START BOT ONCE MY MASTER")

    bot.run()
