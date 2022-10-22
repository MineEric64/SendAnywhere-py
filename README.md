# SendAnywhere-py
Send Anywhere Unofficial API for Python

- [한국어 README 문서](./README_ko.md)

## NOTE
Warning!

This SendAnywhere api is **unofficially** made by SendAnywhere user, not SendAnywhere developer.

So this SendAnywhere api developer does not assume any legal responsibility arising from using this api.

**Please consider using SendAnywhere official api.**

## Usage
### SendClass
|Method|Description|Parameter|Returns|
|:---:|:---:|:---:|:---:|
|`SendClass(paths, device_key)`|Initialize for sending files.|`paths`: list (that has str), `device_key`: str, `device_key` is already declared by default.|.|
|`send()`|Send Files that are in `paths`.|.|.|
|`send_with_key()`|Send Files that are in `paths`.|.|returns key. (`key` type: int)|
|`send_with_key_to_string()`|Send Files that are in `paths`.|.|returns key to string. (`key` type: string)|
|`send_with_verbose()`|Send Files that are in `paths`, you can see more details info about `send()` method. but using this method is not recommended.|.|`verbose` type: dict|
|`fetch()`|Fetch Files to Server. Waiting for receiving (downloading) files from user. You must use fetch method before using receiving method.|.|.|
|`fetch_async()`|Fetch Asynchronously.|.|.|
|`get_key_to_string()`|Get Key that can receive (download) files to string.|.|`key` type: string|
|`has_error()`|Using Sending Method, if error occurs returns `true` otherwise returns `false`.|.|type: `bool`|
|`raise_for_error()`|Using Sending Method, if error occurs raise error.|.|returns `ValueError`|

- You can get key from `key` parameter in SendClass.

### ReceiveClass
|Method|Description|Parameter|Returns|
|:---:|:---:|:---:|:---:|
|`ReceiveClass(key)`|Initialize for receiving (downloading) files.|`key` type: int|.|
|`get_link()`|Get link that is gotten by `key`.|.|`link` type: str|
|`get_link_verbose()`|Get verbose info that is gotten by `key`. but using it is not recommended.|.|`verbose` type: dict|
|`get_key_to_string()`|Get Key that can receive (download) files to string.|.|`key` type: string|

### Example
```python
import requests
import asyncio

import SendAnywhere as sa

# upload (send) files to SendAnywhere Server
# and return key that can download files
async def test_send():
    paths = [] # file paths that will upload to SendAnywhere Server

    while True:
        path: str = input()

        if path == "-1":
            break

        paths.append(path)

    # upload (send) files to Server
    s = sa.SendClass(paths)
    s.send()
    error = s.error_message

    print(f'key: {s.get_key_to_string()}') # get key

    if not s.has_error():
        # fetch files to Server.
        # waiting for receiving (downloading) them from user.
        # you must use this method before using receiving method.
        await s.fetch_async()
    else:
        print(f'error message: {s.error_message}')

# receive files from key
# and download them
def test_recieve():
    test_key = int(input()) # key
    test_file_name = input() # file name (this variable can be empty)

    r = sa.RecieveClass(test_key)
    link = r.get_link()

    print(link) # file link that can download
    print("do you wanna download? (y/n): ", end='')
    
    # download files that is recieved
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
      
        # write file
        open(test_file_name, 'wb').write(req.content)

# convert to unicode file name
def encode_with_file_name(text: str) -> str:
    return text.encode("ISO-8859-1").decode("utf-8")
```
