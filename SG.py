import json
from pyrogram import Client

with open("FILES/config.json", "r",encoding="utf-8") as f:
    DATA         = json.load(f)
    API_ID       = DATA["23418117"]
    API_HASH     = DATA["e93479e4b3eae090bf90a978b14ffc09"]
    BOT_TOKEN    = DATA["7985324600:AAGYiFf26KQftyHwIJI88rHDzD5n5GaOBBU"]
    PHONE_NUMBER = DATA["9685745075"]

user = Client("Scrapper",
              api_id       = API_ID,
              api_hash     = API_HASH ,
              phone_number = PHONE_NUMBER
              )

user.start()


