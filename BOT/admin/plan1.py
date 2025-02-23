import traceback, json
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from datetime import date
from datetime import timedelta
import os

@Client.on_message(filters.command("plan1", [".", "/"]))
async def cmd_plan1(Client, message):
    try:
        user_id     = message.from_user.id  # Keep as integer

        # Construct absolute path for config file (more reliable)
        config_file_path = os.path.join(os.getcwd(), "FILES", "config.json")

        try:
            with open(config_file_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                OWNER_ID = config["OWNER_ID"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            await error_log(f"Config file error: {e}")
            return # Exit early if config is bad


        if user_id != OWNER_ID:  # Corrected admin check (integer comparison)
            resp = """You Don't Have Permission To Use This Command.
Contact Bot Owner @FNxDANGER"""
            await message.reply_text(resp, message.id)
            return

        # Rest of your code (assuming it works correctly) ...
        # Keep user_id as integer where appropriate
        user_id_str = message.text.split(" ")[1] # keep this string as a copy
        paymnt_method      = "CRYPTO"
        registration_check = await getuserinfo(user_id_str)
        registration_check = str(registration_check)
        if registration_check == "None":
            resp = f"""
Starter Plan Activation Failed ❌
━━━━━━━━━━━━━━
User ID :  {user_id_str}
Plan Name: Starter Plan For 7 Days
Reason : Unregistered Users

Status : Failed
"""
            await message.reply_text(resp, message.id)
            return

        await check_negetive_credits(user_id_str)
        await getplan1(user_id_str)
        receipt_id  = await randgen(len=10)
        gettoday    = str(date.today()).split("-")
        yy          = gettoday[0]
        mm          = gettoday[1]
        dd          = gettoday[2]
        today       = f"{dd}-{mm}-{yy}"
        getvalidity = str(date.today() + timedelta(days=7)).split("-")
        yy          = getvalidity[0]
        mm          = getvalidity[1]
        dd          = getvalidity[2]
        validity    = f"{dd}-{mm}-{yy}"

        user_resp = f"""
Thanks For Purchasing Our Starter Plan ✅

ID : {user_id_str}
Plan : Starter
Price : 7$
Purchase Date: {today}
Expiry : {validity}
Validity: 7 Days
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
            await error_log(f"Error sending message to user: {e}")  #Specific error log
            pass

        ad_resp = f"""
Starter Plan Activated ✅
━━━━━━━━━━━━━━
User ID :  {user_id_str}
Plan Name: Starter Plan For 7 Days
Plan Expiry: {validity}

Status : Successfull
        """
        await message.reply_text(ad_resp, message.id)

    except Exception as e:
        import traceback
        await error_log(f"Main function error: {traceback.format_exc()}") #Specific error log and main function error
