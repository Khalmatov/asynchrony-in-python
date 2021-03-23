import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET - Addres Famely IP4 , SOCK_STREAM - поддержка протокола TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # SOL_SOCKET - опция относится к уровню сокета, SO_REUSERADDR - переиспользование адреса,  1 - значение
server_socket.bind(('localhost', 5000)) # привязываем сокет к 5000 порту
server_socket.listen() # постоянно слушай

while True:
	print('Before .accept()')
	# ждем входящее подключение
	clien_socket, addr = server_socket.accept() # извлекаем сокет клиента
	print('Connection from', addr)

	while True:
		# ждем входящее сообщение
		request = clien_socket.recv(400) # 400 - размер буфера сообщения

		if not request: # проверяем на наличие непустого сообщения
			break
		else:
			responce = 'Hello world\n'.encode()
			clien_socket.send(responce)
	print('Outside inner while loop')
	clien_socket.close()