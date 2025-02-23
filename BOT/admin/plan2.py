import traceback, json
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from datetime import date
from datetime import timedelta
import os

@Client.on_message(filters.command("plan2", [".", "/"]))
async def cmd_plan2(Client, message):
    try:  # Outer try
        # *** 1. Load Configuration ***
        try:  # Inner try - CORRECT INDENTATION
            with open("FILES/config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            OWNER_ID = config["owner_info"]["owner_id"]  # Direct access, no list

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Config file error: {e}")
            await message.reply_text("Config file error. Check the logs.", quote=True)  # Quote the original message
            return

        # *** 2. Debugging Prints ***
        print(f"cmd_plan2 triggered")
        print(f"User ID: {message.from_user.id}")  # Print as integer
        print(f"Owner ID: {OWNER_ID}")

        # *** 3. Admin Check ***
        user_id = message.from_user.id  #User Id to check if there's a difference
        if user_id != OWNER_ID:
            resp = """You Don't Have Permission To Use This Command.
Contact Bot Owner @FNxDANGER"""
            await message.reply_text(resp, message.id, quote=True)  # Quote the original message
            return

        # *** 4. Rest of the command logic ***
        try:  # Added try-except for the remaining code
            user_id_str = message.text.split(" ")[1]  # Extract user ID from message
            paymnt_method = "CRYPTO"
            registration_check = await getuserinfo(user_id_str)
            registration_check = str(registration_check)
            if registration_check == "None":
                resp = f"""
Silver Plan Activation Failed ❌
━━━━━━━━━━━━━━
User ID :  {user_id_str}
Plan Name: Silver Plan For 15 Days
Reason : Unregistered Users

Status : Failed
"""
                await message.reply_text(resp, message.id, quote=True) # Quote the original message
                return

            await check_negetive_credits(user_id_str)
            await getplan2(user_id_str)
            receipt_id = await randgen(len=10)
            gettoday = str(date.today()).split("-")
            yy = gettoday[0]
            mm = gettoday[1]
            dd = gettoday[2]
            today = f"{dd}-{mm}-{yy}"
            getvalidity = str(date.today() + timedelta(days=15)).split("-")
            yy = getvalidity[0]
            mm = getvalidity[1]
            dd = getvalidity[2]
            validity = f"{dd}-{mm}-{yy}"

            user_resp = f"""
Thanks For Purchasing Our Silver Plan ✅

ID : {user_id_str}
Plan : Silver
Price : 15$
Purchase Date: {today}
Expiry : {validity}
Validity: 15 Days
Status : Paid ☑️
Payment Method : {paymnt_method}.
Receipt ID : MASTER-{receipt_id}

This is a receipt for your plan.saved it in a Secure Place.This will help you if anything goes wrong with your plan purchases .

Have a Good Day .
- @danger_ccbot
"""
            try:
                await Client.send_message(user_id_str, user_resp)
            except Exception as e:
                print(f"Error sending message: {e}")

            ad_resp = f"""
Silver Plan Activated ✅
━━━━━━━━━━━━━━
User ID :  {user_id_str}
Plan Name: Silver Plan For 15 Days
Plan Expiry: {validity}

Status : Successfull
        """
            await message.reply_text(ad_resp, message.id, quote=True)  # Quote the original message

        except Exception as e:  # Catch any errors in the command logic
            print(f"An error occurred in the command logic: {traceback.format_exc()}")
            await message.reply_text("An error occurred while processing the command.", quote=True)
    except:
        print("I can't read log")
