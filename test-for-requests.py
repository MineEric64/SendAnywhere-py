import requests
import SendAnywhere

# I recommend send '(test) 2. 핵심정보를 담은 발표 형성평가 5월 19일.pdf' this file from send-anywhere.

print("please write the number:")
key = int(input())

r: SendAnywhere.RecieveClass = SendAnywhere.RecieveClass(key)
link = r.get_link()

print(link)