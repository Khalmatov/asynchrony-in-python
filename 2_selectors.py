import socket
import selectors

selector = selectors.DefaultSelector()


def server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET - Addres Famely IP4 , SOCK_STREAM - поддержка протокола TCP
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # SOL_SOCKET - опция относится к уровню сокета, SO_REUSERADDR - переиспользование адреса,  1 - значение
	server_socket.bind(('localhost', 5000)) # привязываем сокет к 5000 порту локалхоста (127.0.0.1)
	server_socket.listen() # сокет находится в режиме активного слушания порта постоянно
	selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection) # регистируемый сокет, ожидаемое событие, связанные данные


def accept_connection(server_socket):
	"""
	Функция запускается при обнаружении нового входящего подключения
	"""
	client_socket, addr = server_socket.accept() # извлекаем сокет клиента
	print('У нас новое подключение с адреса:', addr)
	print('Зарегистрируем клиентский сокет в селекторе и начнем за ним следить')
	selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
	"""
	Функция запускается при обнаружении нового сообщения от клиента
	"""
	request = client_socket.recv(4096) # обнаруженный запрос, 4096 - это размер буфера сообщения

	if request:
		print('Клиент нам что-то написал, ответим ему "хэллоу ворд"')
		responce = 'Hello world\n'.encode()
		client_socket.send(responce)
	else:
		print('Пришел пустой запрос, отключаемся от клиента и перестаем за ним следить')
		selector.unregister(client_socket)
		client_socket.close()


def event_loop():
	"""
	Родительская функция, которая следит за изменением состояния сокетов и запускает определенные функции
	"""

	print('Программа запущена')

	while True:

		print('Ждем изменения файлов')
		events = selector.select() # (key, events)
		print('Какой-то файл изменился..')

		for key, _ in events:
			callback = key.data # обратно получаем свою функцию
			callback(key.fileobj) # передаем туда сам сокет


if __name__ == '__main__':
	server()
	event_loop()