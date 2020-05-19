import os
import requests
import json

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

        request = requests.post('https://send-anywhere.com/web/key/search/' + str(self.__key).zfill(6), headers=headers)
        return request.json()

class SendClass:
    key: int = -1
    __file_paths: list

    error_dict: dict = dict()
    error_message: str = "None"

    def __init__(self, path: list):
        self.__file_paths = path

    def send_file_with_key(self) -> int:
        '''
        Send file(s) to send anywhere server and get key.

        :return: returns key number.
        '''

        self.__send_file()
        return self.key

    def send_file_with_verbose(self) -> dict:
        '''
        Send file(s) with Verbose (advanced option)

        :return: returns json (dictionary type)
        '''

        return self.__send_file()

    def __send_file(self) -> dict:
        '''
        Send file(s).

        :return: returns json (dictionary type)
        '''

        files: dict = dict()

        headers: dict = {
            'cookie': 'device_key=3c1f66d0dda7282d49c740d5e938a7caa2c0af60a3731de17677f007811753eb; access_token=NTQ3NDM2NTkzNTI1MzoxNTg5MTI2MDI3Mzcw; _gat=1',
            'Content-Disposition': 'attachment; filename="hello.png"',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }

        for i in range(0, len(self.__file_paths)):
            file_path = self.__file_paths[i]
            file_name = os.path.basename(file_path)

            files[file_name] = open(file_path, 'rb')

        r = requests.post('https://send-anywhere.com/web/key', headers=headers, data=f)
        json_data = r.json()

        if 'key' in json_data:
            self.key = json_data['key']

            self.error_dict = dict()
            self.error_message = "None"
        elif 'error' in json_data:
            self.key = -1

            self.error_dict = json_data
            self.error_message = "error: " + str(json_data['error'])
            return json_data

        #  request send started
        link: str = str(json_data['weblink'])
        link = link[0:link.index('/api/') + 5] + 'session_start/{}?device_key={}'.format(self.key, '3c1f66d0dda7282d49c740d5e938a7caa2c0af60a3731de17677f007811753eb')

        request = requests.post(link)
        print(request.json())

        return json_data