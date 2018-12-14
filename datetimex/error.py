class WrongfulError(Exception):
	"""定义异常,此类为传入字符不合法异常，无法正常转换为数字时间"""
	def __init__(self,err='Unknown error.'):
		Exception.__init__(self,err)