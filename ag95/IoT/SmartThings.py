import requests
from typing import Literal
from pprint import pprint

SMART_THINGS_API_ROOT = 'https://api.smartthings.com/v1'

class SmartThingsControl:
    def __init__(self,
                 token: str):

        authorization = f'Bearer {token}'
        headers = {"Authorization": authorization}
        self.headers = headers

    def get_all_devices(self):
        r = requests.get(f'{SMART_THINGS_API_ROOT}/devices',
                headers=self.headers)
        return r.json()

    def get_status(self,
                   deviceID : str):
        r = requests.get(f'{SMART_THINGS_API_ROOT}/devices/{deviceID}/status',
                headers=self.headers)
        return r.json()

    def TurnSwitch(self,
                   deviceID: str,
                   command: Literal['on', 'off']):
        r = requests.post(f'{SMART_THINGS_API_ROOT}/devices/{deviceID}/commands',
                          headers=self.headers,
                          json={"commands": [
                              {
                                  "component": "main",
                                  "capability": "switch",
                                  "command": command,
                                  "arguments": []
                              }
                          ]})
        return r.json()

if __name__ == '__main__':

    API_intfc = SmartThingsControl(token='your_token')

    # get all devices
    pprint(API_intfc.get_all_devices())

    # get the status of a single device
    # pprint(API_intfc.get_status(deviceID='your_device_ID'))

    # switch a device on/ off
    # pprint(API_intfc.TurnSwitch(deviceID='your_device_ID',
    #                            command='on'))

    print('MANUAL assessment required !')