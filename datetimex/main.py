from datetimex import getTime
from datetimex.error import WrongfulError 
from datetimex.formatTime import FormatTime
from datetimex.formatChinese import FormatChinese
from datetimex.legalizationTime import LegalizationTime


def getTimeString(strTime):
	"""
	将传入的中文时间字符串转换为包含有的数字字符串
	例如：传入值："三年之后"，传出值：“3年之后”
	如果其中出现异常，直接给外部抛出字符串不合法异常　
	"""
	formatStrTimeObject = FormatChinese()
	try:
		timeStr = formatStrTimeObject.format(strTime)
	except Exception as e:
		raise WrongfulError('The incoming string is illegal and cannot be converted to digital time')
	return timeStr

def getTimeData():
	"""
	获取初步处理时间，传出值为tuple，传出值子项也是tuple
	例如：((None, None), (None, None), ('天', -2), (None, None), (None, None), ('早上', 0), ('点', -3), ('半', 0.5), (None, None))
	其中分别为（年，月，日，周数，星期，上下午，时，分秒）的初步处理结果
	如果其中所有子项都为None,抛出字符串不合法异常
	"""
	year = getTime.GetYear().get()
	month = getTime.GetMonth().get()
	day = getTime.GetDay().get()
	weekNum = getTime.GetWeekNum().get()
	week = getTime.GetWeek().get()
	ampm = getTime.GetAmPm().get()
	hour = getTime.GetHour().get()
	minute = getTime.GetMinute().get()
	second = getTime.GetSecond().get()
	if (year[0] == None and year[1] == None and month[0] == None and month[1] == None and day[0] == None and day[1] == None
		and weekNum[0] == None and weekNum[1] == None and week[0] == None and weekNum[1] == None and ampm[0] == None and ampm[1] == None
		and hour[0] == None and hour[1] == None and minute[0] == None and minute[1] == None and second[0] == None and second[1] == None):
		raise WrongfulError('The incoming string is illegal and cannot be converted to digital time')
	return (year,month,day,weekNum,week,ampm,hour,minute,second)


def getTimeFormatData(timeData,now):
	"""
	获取二次处理时间结果，传入值为初步处理得到的tuple，传出值类型为string
	例如：2018|12|11|X|X|AM|07|30|29
	其中|为方便后续分割字符串所用，这步处理结果可能包含负数，X为没有处理到这部分数据，一般出现在周数和星期
	周数和星期为X时，需要后续进一步处理
	"""
	formatTimeObject = FormatTime(timeData,now)
	try:
		time = formatTimeObject.format()
	except Exception as e:
		raise WrongfulError('The incoming string is illegal and cannot be converted to digital time')
	return time

def getLegalizationTime(time,timeNow):
	"""
	获取三次处理时间结果，传入值为二次处理得到的string，传出值为string
	例如：20181211492AM073029
	其中，2018为处理后的年，12为处理后的月，11为处理后的日，49为当前年的第几周【00为一年中的第一周】，2为星期几【0为星期天，一周的第一天】，
		 AM为上下午，07为时，30为分，29为秒
	一般情况下，到这个方法执行完得到的结果为已经合法的结果，如果为不合法的结果，说明程序已经出现了未知bug

	"""
	LegalizationTimeObject = LegalizationTime()
	try:
		time = LegalizationTimeObject.legalization(time,timeNow)
	except Exception as e:
		raise WrongfulError('The incoming string is illegal and cannot be converted to digital time')
	return time

def main(timeStr,now):
	strTime = getTimeString(timeStr)							#先将传入的字符串转换其中的中文数字为阿拉伯数字
	getTime.timeString = strTime
	getTime.now = now
	getFirstTimeData = getTimeData()									#获取初步处理结果
	formatTimeData = getTimeFormatData(getFirstTimeData,now)			#获取二次处理结果
	legalizationTimeData = getLegalizationTime(formatTimeData,now)		#获取时间合法化后的结果
	return legalizationTimeData
