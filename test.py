# -*- coding: UTF-8 -*-

import requests
import asyncio

import SendAnywhere

async def test_send():
    paths = []

    while True:
        path: str = input()

        if path == "-1":
            break

        paths.append(path)

    s: SendAnywhere.SendClass = SendAnywhere.SendClass(paths)
    s.send()
    error = s.error_message

    print(f'key: {s.get_key_to_string()}')

    if not s.has_error():
        await s.fetch_async()
    else:
        print(f'error message: {s.error_message}')

def test_recieve():
    test_key = int(input())
    test_file_name = input()

    r: SendAnywhere.RecieveClass = SendAnywhere.RecieveClass(test_key)
    link = r.get_link()

    print(link)
    print("do you wanna download? (y/n): ", end='')

    if input() == "y" and not link.startswith("error: "):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-type': 'text/plain; charset=utf-8'
        }

        req = requests.get(link, headers=headers, allow_redirects=True)  # download

        if req.status_code != 200:
            return

        if test_file_name == "":
            test_file_name = encode_with_file_name(req.headers['Content-Disposition'].split("filename=")[1].strip('"'))
            print(test_file_name)

        #open(test_file_name, 'wb').write(req.content)

def encode_with_file_name(text: str) -> str:  # "2119ë ê°ë½ì¤íêµ íêµ.mp3"
    return text.encode("ISO-8859-1").decode("utf-8")

f_name = input()

if f_name is "s":  # send
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_send())
elif f_name is "r":  # recieve
    test_recieve()

#test_send()
#test_recieve()