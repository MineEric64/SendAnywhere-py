import requests

import SendAnywhere

def test_recieve():
    test_key = int(input())
    test_file_name = input()

    r: SendAnywhere.RecieveClass = SendAnywhere.RecieveClass(test_key)
    link = r.get_link()

    print(link)

    if not link.startswith("error: "):
        req = requests.get(link, allow_redirects=True)  # download
        open(test_file_name, 'wb').write(req.content)

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