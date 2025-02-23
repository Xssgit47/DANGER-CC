import traceback, json
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from datetime import date, timedelta, datetime
import os

@Client.on_message(filters.command("plan2", [".", "/"]))
async def cmd_plan2(Client, message):
    try:  # Outer try encompassing everything except config loading
        # * 1. Load Configuration *
        try:
            with open("FILES/config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            OWNER_ID = int(config["OWNER_ID"])  # Direct access
        except FileNotFoundError:
            print("Config file not found.")
            await message.reply_text("Config file not found.", quote=True)
            return
        except json.JSONDecodeError:
            print("Invalid JSON in config file.")
            await message.reply_text("Invalid JSON in config file.", quote=True)
            return
        except KeyError as e:
            print(f"Missing key in config file: {e}")
            await message.reply_text("Missing key in config file. Check the logs.", quote=True)
            return
        except Exception as e:
            print(f"Unexpected error loading config: {e}")
            await message.reply_text("Unexpected error loading config. Check the logs.", quote=True)
            return

        # * 2. Debugging Prints *
        print("cmd_plan2 triggered")
        print(f"User ID: {message.from_user.id}")
        print(f"Owner ID: {OWNER_ID}")

        # * 3. Admin Check *
        user_id = message.from_user.id  #User Id to check if there's a difference
        if user_id != OWNER_ID:
            resp = """You Don't Have Permission To Use This Command.
Contact Bot Owner @FNxDANGER"""
            await message.reply_text(resp, message.id, quote=True)  # Quote the original message
            return

        # * 4. Rest of the command logic *
        try:
            user_id_str = message.text.split(" ")[1]  # Extract user ID from message
            try:
                user_id_to_activate = int(user_id_str)  # Convert to integer immediately
            except ValueError:
                await message.reply_text("Invalid user ID provided.", quote=True)
                return

            paymnt_method = "CRYPTO"

            registration_check = await getuserinfo(user_id_to_activate)
            if registration_check is None:  #Check if None
                resp = f"""
Silver Plan Activation Failed ❌
━━━━━━━━━━━━━━
User ID :  {user_id_str}
Plan Name: Silver Plan For 15 Days
Reason : Unregistered Users

Status : Failed
"""
                await message.reply_text(resp, message.id, quote=True)
                return

            await check_negetive_credits(user_id_to_activate)
            await getplan2(user_id_to_activate)
            receipt_id = await randgen(len=10)

            today_date = date.today()
            validity_date = today_date + timedelta(days=15)

            today = today_date.strftime("%d-%m-%Y")  # Use strftime
            validity = validity_date.strftime("%d-%m-%Y")

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
                await Client.send_message(user_id_to_activate, user_resp)
            except Exception as e:
                print(f"Error sending message to user: {e}")
                await message.reply_text(f"Error sending message to user: {e}", quote=True) # Inform Admin

            ad_resp = f"""
Silver Plan Activated ✅
━━━━━━━━━━━━━━
User ID :  {user_id_str}
Plan Name: Silver Plan For 15 Days
Plan Expiry: {validity}

Status : Successfull
"""
            await message.reply_text(ad_resp, message.id, quote=True)

        except Exception as e:
            error_message = f"An error occurred: {e}\n{traceback.format_exc()}"
            print(error_message)
            await message.reply_text(f"An error occurred: {e}. Check the logs.", quote=True)

    except Exception as e:
        print(f"Unexpected Error: {e}") # Catch all errors.
