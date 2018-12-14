import calendar
from datetime import datetime

class LegalizationTime(object):
	"""这个类用作时间的合法化处理"""
	def __init__(self):
		super(LegalizationTime, self).__init__()
		self.__time = None
		self.__year = None
		self.__month = None
		self.__day = None
		# self.__weekNum = None
		self.__week = None
		self.__ampm = None
		self.__hour = None
		self.__minute = None
		self.__second = None

		self.__year_offset = 0
		self.__month_offset = 0
		self.__day_offset = 0
		# # self.__weekNum_offset = 0
		# self.__week_offset = 0
		self.__ampm_offset = 0
		self.__hour_offset = 0
		self.__minute_offset = 0
		self.__second_offset = 0

	def legalization(self,timeData,timeNow):
		"""
			供给外部调用的合法化方法，
			传入参数为formatTime.py中取得的时间字符串，样式为类似于：2018-12-10-X-X-XX-07-59-86
			这里将传入的初步处理时间数据按照符号‘|’来进行切割，将结果传给类属性self.__time，切割后的元组类似于：['2018', '12', '10', 'X', 'X', 'XX', '08', '04', '61']
		"""
		time = None
		self.__time = timeData.split('|')
		self.__legalizationSecond()
		self.__legalizationMinute()
		self.__legalizationHour()
		self.__legalizationAmPm()
		self.__legalizationWeek(timeNow)						#这个方法用作周数和星期的合法化，年月日合法化方法在此方法内，具体原因请看此方法的描述
		time = self.__year + self.__month + self.__day + self.__week +  self.__ampm + self.__hour + self.__minute + self.__second
		return time

	def __legalizationSecond(self):
		"""进行秒的合法化"""
		second = int(self.__time[-1])									#秒数为最后一个子项
		if second >= 60 or second < 0:
			self.__minute_offset = second // 60
			self.__second = self.__formatLength(second % 60)
		else:
			self.__second = self.__formatLength(second)

	def __legalizationMinute(self):
		"""进行分的合法化,执行操作前，需要把上一步得到的偏移量加到该变量中"""
		minute = int(self.__time[-2]) + self.__minute_offset			#分数为倒数第二个子项
		if minute >= 60 or minute < 0:
			self.__hour_offset = minute // 60
			self.__minute = self.__formatLength(minute % 60)
		else:
			self.__minute = self.__formatLength(minute)


	def __legalizationHour(self):
		"""进行时的格式化,执行操作前，需要把上一步得到的偏移量加到该变量中"""
		hour = int(self.__time[-3]) + self.__hour_offset				#时数为倒数第三个子项
		self.__ampm_offset = hour // 12
		self.__day_offset = hour // 12
		self.__hour = self.__formatLength(hour % 12)
		if self.__hour == '00':											#如果时为00，将00置为12
			self.__hour = '12'

	def __legalizationAmPm(self):
		"""进行上下午的合法化，将上一步取得的偏移量按指定算法合并到变量中"""
		ampm = self.__time[-4]
		if self.__ampm_offset % 2 == 0:									#整除，和当前ａｍｐｍ一致，不整除，与当前ａｍｐｍ相反
			self.__ampm = ampm
		else:
			if ampm == 'AM':
				self.__ampm = 'PM'
			else:
				self.__ampm = 'AM'

	def __legalizationDay(self,timeNow):
		if timeNow[11:13] == 'AM':										 
			"""
			当前时间为am时，每隔两个单位的偏移量为新的一天
			例如：当前为am，最近的12点后，am变为pm，但依然是当前这一天，但当再过一次12点时，pm又重新变为am
			开始新的一天	
			"""
			day = int(self.__time[2]) + self.__day_offset // 2		
		else:															
			"""
			当前为pm时，将使用等差数列公式求得通项,#An = A1 +（ｎ－１）＊ｄ，求ｎ，ｎ即要加的天数
			因为假设当前为pm，上面步骤取得的ampm偏移值为每12小时为1的单位，而pm时，偏移量为单数即新的一天，
			例如：1，pm在凌晨00点后应变为am，而且为新的一天，以此类推，得到1，3，5，7，9格式的等差数列，公差为2，首项为1
			因为通过公式变形得到结果对应为1，2，3，4，5天，将这个结果和已经存在的天数相加得到新天数

			"""
			day = int(self.__time[2]) + (self.__day_offset + 1) // 2
		####上面是进行根据时数来计算天数的情况，后续还需要进行天数是否超过了这个月包含的天数，超过的话，要把偏移量算出来保存
		###calendar.monthrange这个方法可以得到某月包含的天数总数，传入：（年，月）返回：（月，天数）,这个库是标准库
		month = int(self.__time[1])
		while 1:
			daySum = calendar.monthrange(int(self.__time[0]) + self.__year_offset,month + self.__month_offset)
			if day > daySum[1] or day < 1:
				if day > daySum[1]:
					day = day - daySum[1]
					self.__month_offset += 1
				elif day < 1:
					daySumTem = calendar.monthrange(int(self.__time[0]) + self.__year_offset,month + self.__month_offset - 1)
					self.__month_offset -= 1
					day = daySumTem[1] + day
				if month + self.__month_offset > 12:
					self.__year_offset += 1
					month = 0
				elif month + self.__month_offset < 1:
					self.__year_offset -= 1
					month = 12
			else:
				break
		self.__day = self.__formatLength(day)

	def __legalizationMonth(self):
		month = int(self.__time[1]) + self.__month_offset
		if month > 12 or month < 1:
			self.__year_offset = month // 12
			self.__month = self.__formatLength(month % 12)
		else:
			self.__month = self.__formatLength(month)

	def __legalizationYear(self):
		year = int(self.__time[0]) + self.__year_offset
		self.__year = self.__formatLength(year)


	def __legalizationWeek(self,timeNow):
		"""
		这个方法用作格式化周数和星期，当二次处理结果没有周数和星期的值时，该位置被置为字符串“X”
		当判断周数和星期为X时，将通过指定的年月日获取到精准的周和星期
		当判断到周数或星期不为X时，将通过周数获取精准的年月日
		"""
		if self.__time[3] == 'X' and self.__time[4] == 'X':					#指定日期 -> 周-星期
			self.__legalizationDay(timeNow)						
			self.__legalizationMonth()
			self.__legalizationYear()
			self.__week = datetime.strptime(self.__year+self.__month+self.__day,"%Y%m%d").strftime("%U%w")
		else:																#周-星期 -> 指定日期
			result = datetime.strptime(self.__time[3]+self.__time[4],"%U%w").strftime("%m%d")
			self.__year = self.__formatLength(self.__time[0])
			self.__month = self.__formatLength(result[:2])
			self.__day = self.__formatLength(result[2:])
			self.__week = self.__time[3]+self.__time[4]
		if int(self.__week[:2]) > 52:											#当周数大于52,这里写死隔一年可计算，多了失效，待后续改善，一年不一定是52周，可能是53
			self.__week = self.__formatLength(int(self.__week) - 52)
			self.__year_offset = 1
			self.__legalizationYear()

	def __formatLength(self,number):
		"""进行时间字符串长度的格式化"""
		number = str(number)
		if len(number) == 1:
			number = '0' + number
		else:
			number = str(number)
		return number