import time
import hashlib
import hmac
import requests
import json
from pprint import pprint
from typing import Literal

class TuyaCloudControl:
    def __init__(self,
                 client_id: str,
                 secret: str):

        self.client_id = client_id
        self.secret = secret

    def _request(self,
                 url: str,
                 request_type: Literal['GET', 'POST'],
                 body: str | dict = '',
                 access_token: str = None):

        now = int(time.time()*1000)
        headers = {'secret': self.secret}

        payload = self.client_id + (access_token or '') + str(now)
        payload += (f'{request_type}\n'
                    f'{hashlib.sha256(bytes((body or '').encode('utf-8'))).hexdigest()}\n'        # body or ''
                    f'{''.join([f'{key}:{headers[key]}\n'                                         # Signature-Headers
                                for key in headers.get("Signature-Headers", '').split(":")
                                if key in headers])}\n'
                    f'{'/' + url.split('//', 1)[-1].split('/', 1)[-1]}') # the leftmost URL, for ex /v1.0/token?grant_type=1

        # Sign Payload
        signature = hmac.new(
            key=self.secret.encode('utf-8'),
            msg=payload.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest().upper()

        # Create Header Data
        headers['client_id'] = self.client_id
        headers['sign'] = signature
        headers['t'] = str(now)
        headers['sign_method'] = 'HMAC-SHA256'
        headers['mode'] = 'cors'
        if access_token: headers |= {'access_token': access_token}

        try:
            return (requests.get(url, headers=headers).json()) if request_type == 'GET'\
                else (requests.post(url, headers=headers, data=body).json())
        except:
            return None

    def get_access_token(self):
        """Retrieve the access token from Tuya API.
        This token is needed on top of the api key and secret.
        Not sure why tTuya decided to do it this way, but it is what it is ..."""

        try:
            response = self._request(url='https://openapi.tuyaeu.com/v1.0/token?grant_type=1',
                                     request_type='GET',
                                     body={},
                                     access_token=None)

            if response and response['success']:

                return {'access_token': response['result']['access_token'],
                        'expire_time': response['result']['expire_time'],
                        'refresh_token': response['result']['refresh_token']}

            else:
                return {'access_token': None,
                        'expire_time': None,
                        'refresh_token': None}
        except:
            return {'access_token': None,
                    'expire_time': None,
                    'refresh_token': None}

    def get_status(self,
                   device_id: str,
                   access_token: str):

        try:
            response = self._request(url=f'https://openapi.tuyaeu.com/v1.0/iot-03/devices/{device_id}/status',
                                     request_type='GET',
                                     body={},
                                     access_token=access_token)

            if response and response['success']:
                state_descriptor = [_ for _ in response['result'] if _['code'] == 'switch_1']
                if state_descriptor:
                    return {'state': state_descriptor[0]['value']}
                else:
                    return {'state': None}

            else:
                return {'state': None}

        except:
            return {'state': None}

    def TurnSwitch(self,
                   device_id: str,
                   access_token: str,
                   command: Literal['on', 'off']):

        try:
            response = self._request(url=f'https://openapi.tuyaeu.com/v1.0/iot-03/devices/{device_id}/commands',
                                     request_type='POST',
                                     body=json.dumps({"commands": [{"code": "switch_1", "value": True if command == 'on' else False}]}),
                                     access_token=access_token)

            if response and response['success']:
                return {'result': response['result']}

            else:
                return {'result': None}

        except:
            return {'result': None}

if __name__ == '__main__':

    # # initialize the API interface
    # API_intfc = TuyaCloudControl(client_id = '<your_client_ID>',
    #                              secret = '<your_secret>')
    #
    # get an access token
    # pprint(API_intfc.get_access_token())
    #
    # # get the status of a single device
    # pprint(API_intfc.get_status(device_id = '<your_device_ID>',
    #                            access_token = API_intfc.get_access_token()['access_token']))
    #
    # # switch a device on/ off
    # pprint(API_intfc.TurnSwitch(device_id = '<your_device_ID>',
    #                             access_token = API_intfc.get_access_token()['access_token'],
    #                             command='on'))

    print('MANUAL assessment required !')