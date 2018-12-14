import time
from datetimex import main
from datetimex.error import WrongfulError 



"""
执行流程：
	1.程序入口											main.py
	2.中文数字转换成对应数字 								formatChinese.py
	3.获取字符串中的时间	  								getTime.py
	4.格式化时间，将2中获取到的数值进行进一步格式化			formatTime.py
	5.将3中获取到的时间进行合法化							legalizationTime.py
"""


def gettime(strTime):
	"""
	这个方法为外部调用这个库所用方法
	传入一个正确包含中文时间的时间字符串，例如：明天中午十二点、两天后的早上七点等
	返回一个元组，第一项为当前时间格式化后的字符串，第二个为传入带中文的字符串格式化后的字符串，例如：('20181214495PM042101', '20181130475PM040000')
	其中，前四位代表年，5、6位代表月，7、8位代表日，9、10位代表周数(一年内所在的第几周),11位代表星期几(星期天为一周第一天，为０),12、13代表上下午
		14、15代表时，16、17代表分，18，19位代表秒
	"""
	timestamp=int(time.time())
	format_timestamp = time.localtime(int(time.time()))
	time_now = time.strftime("%Y%m%d%U%w%p%I%M%S", format_timestamp)				##格式：年月日周星期时分秒(12小时制)
	return_time = main.main(strTime,time_now)
	return (time_now,return_time)