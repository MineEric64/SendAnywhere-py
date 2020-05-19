# -*- coding: UTF-8 -*-

import requests

import SendAnywhere

def test_recieve():
    test_key = int(input())
    test_file_name = input()

    r: SendAnywhere.RecieveClass = SendAnywhere.RecieveClass(test_key)
    link = r.get_link()

    print(link)

    if not link.startswith("error: "):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-type': 'text/plain; charset=utf-8'
        }

        req = requests.get(link, headers=headers, allow_redirects=True)  # download

        if req.status_code != 200:
            return

        if test_file_name == "":
            test_file_name = req.headers['Content-Disposition'].split("filename=")[1].strip('"')
            print(test_file_name)

        #open(test_file_name, 'wb').write(req.content)

def test_send():
    paths: list = list()

    while True:
        path: str = input()

        if path == "-1":
            break

        paths.append(path)

    s: SendAnywhere.SendClass = SendAnywhere.SendClass(paths)
    key = s.send_file_with_key()
    error = s.error_message

    print(key)
    print(error)

test_send()
#test_recieve()

# text = "2119ë ê°ë½ì¤íêµ íêµ.mp3"
# text2 = "2119년 가락중학교 폐교.mp3"
#
# # for i in range(0, len(text)):
# #     print("{0:b}".format(ord(text[i])))
#
# for i in range(0, len(text)):
#     print(ord(text[i]))