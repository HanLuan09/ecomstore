from ecomstore import settings
import http.client
import urllib.parse

def do_auth_capture(amount='0.00', card_num=None, exp_date=None, card_cvv=None):
    delimiter = '|'
    raw_params = {
        'x_login': settings.AUTHNET_LOGIN,
        'x_tran_key': settings.AUTHNET_KEY,
        'x_type': 'AUTH_CAPTURE',
        'x_amount': amount,
        'x_version': '3.1',
        'x_card_num': card_num,
        'x_exp_date': exp_date,
        'x_delim_char': delimiter,
        'x_relay_response': 'FALSE',
        'x_delim_data': 'TRUE',
        'x_card_code': card_cvv
    }

    params = urllib.parse.urlencode(raw_params).encode('utf-8')
    headers = {'content-type': 'application/x-www-form-urlencoded', 'content-length': len(params)}

    post_url = settings.AUTHNET_POST_URL
    post_path = settings.AUTHNET_POST_PATH

    with http.client.HTTPSConnection(post_url, http.client.HTTPS_PORT) as cn:
        cn.request('POST', post_path, params, headers)
        return cn.getresponse().read().decode('utf-8').split(delimiter)
