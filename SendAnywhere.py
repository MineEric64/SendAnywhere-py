import os
import requests
import json

import datetime
import asyncio

class SendClass:
    key: int = -1
    __file_paths: list

    __device_key: str
    __default_device_key = '3c1f66d0dda7282d49c740d5e938a7caa2c0af60a3731de17677f007811753eb'
    __session_start_link: str

    error_dict = {}
    error_message = "None"

    def __init__(self, path: list, device_key: str = __default_device_key):
        self.__file_paths = path
        self.__device_key = device_key

    def send(self):
        self.__send()

    def send_with_key(self) -> int:
        self.__send()
        return self.key

    def send_with_key_to_string(self) -> str:
        self.__send()
        return self.get_key_to_string()

    def send_with_verbose(self):
        return self.__send()

    def __send(self) -> dict:
        '''
        Send and Upload file(s) To Send-Anywhere File Server.

        :return: returns json (dictionary type)
        '''

        files = {}

        headers = {
            'cookie': f'device_key={self.__device_key}; access_token=NTQ3NDM2NTkzNTI1MzoxNTg5MTI2MDI3Mzcw; _gat=1',
        }

        # for i in range(0, len(self.__file_paths)):
        #     file_path = self.__file_paths[i]
        #     file_name = os.path.basename(file_path)
        #
        #     files[file_name] = open(file_path, 'rb')

        req = requests.post('https://send-anywhere.com/web/key', headers=headers, files={"file": open("hello.png", "rb")}, json={"file":[{"name": "hello.png", "size": os.stat("hello.png").st_size}]})
        json_data = req.json()

        if 'key' in json_data:
            self.key = int(json_data['key'])

            self.error_dict = {}
            self.error_message = "None"
        elif 'error' in json_data:
            self.key = -1

            self.error_dict = json_data
            self.error_message = f"error: {str(json_data['error'])}"
            return json_data

        link: str = str(json_data['weblink'])
        self.__session_start_link = f"{link[0:link.index('/api/') + 5]}session_start/{self.get_key_to_string()}"

        return json_data

    def fetch(self):
        '''
        fetch file(s) to Send-Anywhere Server. You must fetch them before recieve (or download) them. (Synchronous)
        '''
        self.__upload_for_fetch()

    async def fetch_async(self):
        '''
        fetch file(s) to Send-Anywhere Server. You must fetch them before recieve (or download) them. (Asynchronous)
        '''
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.__upload_for_fetch)

    def __upload_for_fetch(self):
        session_link = self.__session_start_link.replace("/session_start/", "/session/", 1)
        session_finish_link = self.__session_start_link.replace("/session_start/", "/session_finish/", 1)
        data_upload_link = f'{session_link[:session_link.index("/session/") + 9]}file/'
        file_key: str

        req_session_start = requests.get(self.__session_start_link, params={'device_key': self.__device_key}, json={"file": [{"name": "hello.png", "size": os.stat("hello.png").st_size}]})
        file_key = req_session_start.json()['file'][0]['key']
        data_upload_link += file_key

        requests.post(data_upload_link, params={'device_key': self.__device_key, 'offset': 0}, files={"file" : open('hello.png', 'rb')})

        requests.get(session_link, params={'device_key': self.__device_key, 'mode': 'status', '_': int(datetime.datetime.utcnow().timestamp())})
        requests.get(session_finish_link, params={'device_key': self.__device_key, 'mode': 'status', '_': int(datetime.datetime.utcnow().timestamp())})

    def get_key_to_string(self) -> str:
        return str(self.key).zfill(6)

    def has_error(self) -> bool:
        return self.error_message is not "None" or len(self.error_dict) is not 0

    def raise_for_error(self):
        if self.has_error():
            raise ValueError("Error occured.")

class RecieveClass:
    __key: int

    def __init__(self, key: int):
        self.__key = key

    def get_link(self) -> str:
        response = self.__get_response()
        if 'error' in response:
            return 'error: ' + response['error']

        return response['weblink']

    def get_link_verbose(self) -> dict:
        return self.__get_response()

    def __get_response(self) -> dict:
        headers = {
            'authority': 'send-anywhere.com',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://send-anywhere.com',
            'referer': 'https://send-anywhere.com/ko',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'cookie': 'device_key=3c1f66d0dda7282d49c740d5e938a7caa2c0af60a3731de17677f007811753eb; access_token=NTQ3NDM2NTkzNTI1MzoxNTg5MTI2MDI3Mzcw; _gat=1'
        }

        request = requests.post(f'https://send-anywhere.com/web/key/search/{self.get_key_to_string()}', headers=headers)
        return request.json()

    def get_key_to_string(self):
        '''
        Get Key with String.

        :return: returns key with string.
        '''
        return str(self.__key).zfill(6)