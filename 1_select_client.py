import socket

req = b'Hello server!'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET указывает, что мы будем работать с сетевыми сокетами
# SOCK_STREAM указывает, что мы будем работать по протоколу TCP

s.connect(('127.0.0.1', 5000)) # подключение к хосту с портом (начинается тройное рукопожатие: SYN>SYN-ACK>ACK)

s.send(req) # отправка сообщения серверу

rsp = s.recv(4096) # получение ответного сообщения от сервера

print(rsp.decode('utf-8')) # декодируемые байтовые строки в str

s.close() # закрываем соединение