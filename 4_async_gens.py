import socket
from select import select

tasks = []

to_read = {}
to_write = {}

def server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET - Addres Famely IP4 , SOCK_STREAM - поддержка протокола TCP
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # SOL_SOCKET - опция относится к уровню сокета, SO_REUSERADDR - переиспользование адреса,  1 - значение
	server_socket.bind(('localhost', 5000)) # привязываем сокет к 5000 порту
	server_socket.listen() # постоянно слушай

	while True:

		print('Исполняю задачу: добавляю серверный сокет в мониторинг "чтения"')
		yield ('read', server_socket)
		client_socket, addr = server_socket.accept() # read # извлекаем сокет клиента

		print('Исполняю задачу: создан клиентский сокет с адресом:', addr)

		tasks.append(client(client_socket))


def client(client_socket):
	while True:

		print('Исполняю задачу: добавляю клиентский сокет в мониторинг "чтения"')
		yield ('read', client_socket)
		# ждем входящее сообщение
		request = client_socket.recv(4096) # read -  400 - размер буфера сообщения

		if not request: # проверяем на наличие непустого сообщения
			print('Клиент отправил пустой запрос')
			break
		else:
			print('Исполняю задачу: ')
			print('Клиент нам что-то написал, отправим ему хэллоу ворлд')
			responce = 'Hello world\n'.encode()

			print('Добавляю клиентский сокет в мониторинг "записи"')
			yield ('write', client_socket)
			client_socket.send(responce)  # write

	print('Вырубаю клиентский сокет')
	client_socket.close()


def event_loop():

	print('Программа запущена и будет выполнятся, пока не иссякнут списки задач или мониторинга')
	while any([tasks, to_read, to_write]):

		while not tasks:
			print('Задачи не обнаружены. Слежу за изменениями сокетов\n')
			ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
			print('Что-то изменилось. Пойду, посмотрю, что там')

			for sock in ready_to_read:
				print('Изменился сокет на чтение')
				tasks.append(to_read.pop(sock))

			for sock in ready_to_write:
				print('Изменился сокет на запись')
				tasks.append(to_write.pop(sock))

		try:
			print('Обнаружена задача, извлекаю ее')
			task = tasks.pop(0)

			reason, sock = next(task)

			if reason == 'read':
				to_read[sock] = task
			if reason == 'write':
				to_write[sock] = task
		except StopIteration:
			print('Клиент, похоже, отключился')

if __name__ == '__main__':
	tasks.append(server())
	event_loop()