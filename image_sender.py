import requests

img = []
with open('test_images/img4.jpg', 'rb') as f:
    img = f.read()
print(len(img))
response = requests.post('http://127.0.0.1:8000/detector/', files={'image':img})
# при приёма на стороне сервера нужно ещё раз вызвать метод read() для получения байтов

print(response.status_code)
print(response.json())