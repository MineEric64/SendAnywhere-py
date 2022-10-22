# SendAnywhere-py
파이썬용 Send Anywhere 비공식 API

- [English README Documentation](./README.md)

## 공지
주의!

이 SendAnywhere API는 SendAnywhere 개발자가 아닌 SendAnywhere 유저가 만든 **비공식** API입니다.

따라서 SendAnywhere API 개발자는 이 API를 사용하므로써 어느 법적 책임도 지지 않습니다.

**SendAnywhere 공식 API를 사용하는 것을 권장합니다.**

## 사용법
### SendClass
|함수|설명|매개 변수|반환값|
|:---:|:---:|:---:|:---:|
|`SendClass(paths, device_key)`|파일을 보내기 위해 초기화합니다.|`paths`: (문자열 (str)을 가지고 있는) list, `device_key`: str, `device_key`는 기본값에 의해 설정됨|.|
|`send()`|`paths`에 있는 파일을 보냅니다.|.|.|
|`send_with_key()`|`paths`에 있는 파일을 보냅니다.|.|key를 반환합니다. (`key` 타입: int)|
|`send_with_key_to_string()`|`paths`에 있는 파일을 보냅니다.|.|key를 문자열로 반환합니다. (`key` 타입: string)|
|`send_with_verbose()`|`paths`에 있는 파일을 보냅니다, `send()` 함수에 대해 더 많은 정보를 볼 수 있습니다. 하지만 이 함수를 사용하는 것은 추천하지 않습니다.|.|`verbose` 타입: dict|
|`fetch()`|서버에 파일을 패치합니다. 유저가 파일을 받는 것을 기다립니다. Receive 함수를 쓰기 전에 반드시 패치 함수를 사용해야 합니다.|.|.|
|`fetch_async()`|비동기적으로 패치합니다.|.|.|
|`get_key_to_string()`|파일을 받을 수 있는 key를 문자열로 가져옵니다.|.|`key` 타입: string|
|`has_error()`|Send 함수를 사용하면서, 오류가 발생하면 `true`를 반환하고 그렇지 않으면 `false`를 반환합니다.|.|타입: `bool`|
|`raise_for_error()`|Send 함수를 사용하면서, 오류가 발생하면 오류를 raise (throw)합니다.|.|`ValueError`를 반환합니다.|

- SendClass에 있는 `key` 변수로 key를 가져올 수 있습니다.

### ReceiveClass
|함수|설명|매개 변수|반환값|
|:---:|:---:|:---:|:---:|
|`ReceiveClass(key)`|파일을 받기 위해 초기화합니다.|`key` 타입: int|.|
|`get_link()`|`key`로 가져온 파일 다운로드 링크를 가져옵니다.|.|`link` 타입: str|
|`get_link_verbose()`|`key`로 가져온 자세한 (verbose) 정보를 가져옵니다. 하지만 사용하는 것은 추천하지 않습니다.|.|`verbose` 타입: dict|
|`get_key_to_string()`|파일을 받을 수 있는 key를 문자열로 가져옵니다.|.|`key` : string|

### 예시
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

### 개발 비화
비공식 Send Anywhere API를 만든 계기는 대용량 파일을 폰과 컴퓨터에 보내고 받기 위해 만들게 되었습니다.

원래 Send Anywhere 프로그램을 쓰면 됐지만 Send Anywhere 프로그램 내장 광고가 조금 거슬리기도 했고

무엇보다 제가 만든 프로그램에서 Send Anywhere 프로그램을 키지 않고도 바로 한 번 클릭에 파일이 공유가 되게 만들고 싶었습니다.

- 그러면 그냥 공식 API를 사용하면 되지 않나?
라고 생각하시겠지만,

**맞습니다.**

하지만 그래도 제가 직접 Send Anywhere을 뜯어보며 제가 직접 저의 손으로 API를 만들어보고 싶었습니다.

Send Anywhere 개발자님, 죄송합니다. 문제 시 Repository는 삭제하도록 하겠습니다.

- [더 자세한 개발 비화가 궁금하신가요?](https://github.com/Luigi38/MyPortfolio#send-anywhere-%EB%B9%84%EA%B3%B5%EC%8B%9D-api)
