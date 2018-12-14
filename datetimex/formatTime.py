from datetimex.error import WrongfulError 



class FormatTime(object):
	"""
		这个类用作格式化getTime方法中获取到的时间,传入类型tuple
	"""
	def __init__(self,timeData,nowTime):
		super(FormatTime, self).__init__()
		self.__timeData = timeData
		self.__now = nowTime
		self.__yearData = self.__timeData[0]
		self.__monthData = self.__timeData[1]
		self.__dayData = self.__timeData[2]
		self.__weekNumData = self.__timeData[3]
		self.__weekData = self.__timeData[4]
		self.__ampmData = self.__timeData[5]
		self.__hourData = self.__timeData[6]
		self.__minuteData = self.__timeData[7]
		self.__secondData = self.__timeData[8]
		self.__minute_offset = 0

	def format(self):
		year = self.__getTimeData(self.__yearData,[0,4],timeType='year',needFormat=False)
		month = self.__getTimeData(self.__monthData,[4,6],timeType='month')
		day = self.__getTimeData(self.__dayData,[6,8],timeType='day')
		weekNum = self.__formatWeek(self.__weekNumData,[8,10],timeType='weekNum')
		week = self.__formatWeek(self.__weekData,[10,11],timeType='week')
		ampm = self.__formatAmPm(self.__ampmData,[11,13])
		hour = self.__getTimeData(self.__hourData,[13,15],timeType='hour')
		minute = self.__formatLength(int(self.__getTimeData(self.__minuteData,[15,17],timeType='minute')) + self.__minute_offset)
		second = self.__getTimeData(self.__secondData,[17,19],timeType='second')
		time = year + '|' + month + '|' + day + '|' + weekNum + '|' + week + '|' + ampm + '|' + hour + '|' + minute + '|' + second
		return time

	def __formatAmPm(self,timeData,timeIndex):
		ampm = 'XX'
		keyWord =  timeData[0]
		if keyWord:
			if timeData[1] == 0:
				ampm = 'AM'
			elif timeData[1] == 1:
				ampm = 'PM'
			else:
				pass
		else:
			ampm = self.__now[timeIndex[0]:timeIndex[1]]
		return ampm

	def __formatWeek(self,timeData,timeIndex,timeType):
		"""格式化周数需要进行另外的处理"""
		week = 'X'
		keyWord = timeData[0]
		if keyWord:
			if timeType != 'week':																		#周数需要计算，星期直接返回
				week = int(self.__now[timeIndex[0]:timeIndex[1]]) + int(timeData[1])
				week = self.__formatLength(week)
			else:
				week = int(timeData[1])
		week = str(week)
		return week

	def __getTimeData(self,timeData,timeIndex,timeType,needFormat=True):
		"""
			这个方法用作进一步格式化传入的时间，注意：此方法不是每个时间数据都调用
			传入：
				timeData(时间数据，类型为tuple)、
				timeIndex(不作处理时按照现在的时间来取时对应的下标，类型为list，例如取出年数据为【0,4】)
				needFormat(是否进行格式化，即调用__formatLength方法，类型为布尔类型，默认为True，即需要进行调用__formatLength方法)
				timeType(时间类型，即传入的时间类型,类型为string，例如：year、hour)
			传出：进一步处理后的时间数据
		"""
		time = None
		keyWord = timeData[0]
		if keyWord:													#0.5为：*点半的情况，应该通过传入值timeType确定是否为hour，如果是，获取当前时，
			if timeData[1] != 0.5: 									#并将类属性minute设置为30，待后续进行相加操作,否则直接设置time为30
				time = int(self.__now[timeIndex[0]:timeIndex[1]]) + int(timeData[1])
			else:
				if timeType == 'hour':
					time = int(self.__now[timeIndex[0]:timeIndex[1]])
					self.__minute = 30
				elif timeType == 'minute':
					time = 30
				else:												#异常情况
					raise WrongfulError('The incoming string is illegal and cannot be converted to digital time')
		else:					#应该这里加上判断是不是没有分或者秒但是有时，例如今晚８点，应该取得分和秒为00，而不是现在的分和秒
			time = self.__now[timeIndex[0]:timeIndex[1]]
			if timeType == 'minute' or timeType == 'second':
				"""
				这里具体实现根据不同情况格式化返回不同情况的分和秒处理
				这里先进行判断是不是执行到格式化分或者秒，如果是，
				判断时数据是否不为None,如果都不是，还需要判断’后‘字是否在时数据关键字中
				这种情况为：假设现在为下午３点１４分，传入字符串为两个小时后，应该格式化为５点１４分，而不是５点００分
				如果为：现在为下午３点１６分，传入字符串“今晚８点”，应该格式化成今晚的８点００而不是今晚的８点１６
				"""
				if self.__timeData[6][0] != None and self.__timeData[6][1] != None:
					if '后' not in self.__timeData[6][0]:
						time = '00'
					elif '后' in self.__timeData[6][0] and '点' in self.__timeData[6][0]:
						time = '00'
		if needFormat == True:
			time = self.__formatLength(time)
		else:
			time = str(time)
		return time


	def __formatLength(self,number):
		"""
			这个方法用作格式化得到的字符串长度,如果长度为1则在字符串前加上一个0，否则转成字符串后返回
			所以在调用前，必须先确认格式化后的数据格式为正确数据格式，比方说不能格式化星期的数值，星期一：不能将“1”变成“01”
		"""
		string = str(number)
		if len(string) == 1:
			string = '0' + string
		return string