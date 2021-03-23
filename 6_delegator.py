def coroutine(func):
	def inner(*args, **kwargs):
		g = func(*args, **kwargs)
		g.send(None)
		return g
	return inner


class BlaBlaException(Exception):
	pass

@coroutine
def subgen():
	while True:
		try:
			message = yield
		except StopIteration:
			# print('Ku-ku')
			break
		else:
			print('-------', message)
	return 'Returned from subgen'

@coroutine
def delegator(g):
	result = yield from g
	print(result)