import re

timeString = ''
now = ''


class DateTimeBaseClass(object):
	"""
		获取对应时间的基类，获取数据包含(年份、月份、日期、周数、星期、上下午、时、分、秒)
		init方法定义所需列表
		*List为要从中根据相应字段截取字符串进行判断所用，其中为有可能出现的关键字。
		后续使用循环判断，为了避免出现先循环到了短字段，
		实际关键字却是长字段的情况（例如：两年后，实际关键字应该为'年后'，如果列表关键字'年'在前，则会造成影响），
		所以，在定义*List时，字段长的放在前面,优先筛选
		*NumDict为具体要规避的关键字字段，通过这些字段需要进行处理具体数值
	"""
	def __init__(self,List,NumDict):
		super(DateTimeBaseClass, self).__init__()
		self.List = List
		self.NumDict = NumDict


	def _getNumber(self,string,keyWord):
		"""
			获取具体的数值，如果抛出异常，说明有关键字，但是没有具体数值，这种情况需要注意；
			如果没有抛出异常，能直接获取到数值，将该数值和当前年份进行计算，得到返回值number
		"""
		number = None
		try:
			getNumber = re.findall('\d+',string,re.S)[-1]
			number = self._formatGetNumber(keyWord,string,getNumber)
		except IndexError as indexError:
			for item in self.NumDict.keys():
				if item in string:
					number = self.NumDict.get(item)
					break
		except Exception as e:
			raise e
		return number

	def _formatGetNumber(self,keyWord,string,number,strIndexList):
		"""此方法接收一个int类型数值，将此数值与当前时间进行计算，得到差值进行返回"""
		if '前' not in string and '后' not in string and '上' not in string and '下' not in string:
			if '小时' in keyWord:
				retNumber = int(number)
			else:
				timeNow = now[strIndexList[0]:strIndexList[1]]
				retNumber = int(number) - int(timeNow)
		else:
			"""
			这里有多种情况，在‘后’这方面，可能为*小时后、*点后、*分钟之后、*分之后
			假设现在为下午1点1分，传入2小时后，传出应该为下午3点01分，传入2点后，传出应该为下午02点00分
			传入五分钟之后，传出应该为下午1点06分，传入五分之后，传出应该为下午1点05分
			"""
			if '前' in string or '上' in string:
				retNumber = int('-'+ str(number))
			elif '后' in string or '下' in string:
				retNumber = int(number)
				if '后' in string:
					if '后' in keyWord:
						if '点' in keyWord:
							retNumber = int(number) - int(now[strIndexList[0]:strIndexList[1]])
						elif '分' in keyWord and '分钟' not in keyWord:
							retNumber = int(number) - int(now[strIndexList[0]:strIndexList[1]])
		return retNumber

	def get(self):
		"""
			循环*List列表，判断如果传入字符串中包含列表中的子项
			如果存在，则退出循环，执行后续操作。因此这里列表定义值时切记长度应由长到短,避免误选中非准确关键字
		"""
		global timeString
		inList = False
		keyWord = None
		number = None
		for item in self.List:
			if item in timeString:
				inList = True
				keyWord = item
				break
		if inList:
			string = timeString.split(keyWord,1)[0] + keyWord
			timeString = timeString.split(keyWord,1)[-1]
			number = self._getNumber(string,keyWord)
		return (keyWord,number)

class GetYear(DateTimeBaseClass):
	"""获取年份的类"""
	def __init__(self):
		self.yearList = ['年之前','年之后','年前','年后','年']
		self.yearNumDict = {
			'大前年':-3,'大后年':3,'前年':-2,
			'去年':-1,'今年':0,'明年':1,
			'后年':2,'半年':0.5
		}
		super(GetYear, self).__init__(self.yearList,self.yearNumDict)

	def _formatGetNumber(self,keyWord,string,number):
		return super()._formatGetNumber(keyWord,string,number,[0,4])

class GetMonth(DateTimeBaseClass):
	"""获取月份的类"""
	def __init__(self):
		self.monthList = ['月之前','月之后','月份','月前','月后','月']
		self.monthNumDict = {
			'上上个月':-2,'下下个月':2,'上个月':-1,
			'这个月':0,'下个月':1,'上月':-1,
			'这月':0,'下月':1
		}
		super(GetMonth, self).__init__(self.monthList,self.monthNumDict)

	def _formatGetNumber(self,keyWord,string,number):
		return super()._formatGetNumber(keyWord,string,number,[4,6])

class GetDay(DateTimeBaseClass):
	"""获取天数类"""
	def __init__(self):
		self.dayList = ['天之前','天之后','日之前','日之后','明早','明晚','今早','今晚','后晚','大后晚','天前','天后','日前','日后','日','号','天']
		self.dayNumDict = {
			'大前天':-3,'大后天':3,'前天':-2,'大后晚':3,
			'后天':2,'昨天':-1,'明天':1,'后晚':2,'明日':1,
			'这天':0,'今天':0,'明早':1,'明晚':1,'今早':0,'今晚':0,
		}
		super(GetDay, self).__init__(self.dayList,self.dayNumDict)

	def _getNumber(self,string,keyWord):
		"""首先判断明早明晚是否在string中，string为包含天数关键字的变量,如果string包含明早或明晚，在timestring前加上早上或晚上给后续获取上下午类进行处理"""
		global timeString
		if '明早' in string or '今早' in string:
			timeString = '早上' + timeString
		elif '明晚' in string or '今晚' in string or '后晚' in string or '大后晚' in string:
			timeString = '晚上' + timeString
		return super()._getNumber(string,keyWord)

	def _formatGetNumber(self,keyWord,string,number):
		return super()._formatGetNumber(keyWord,string,number,[6,8])




class WeekBaseGetClass(object):
	"""获取周数和星期几的基类"""
	def __init__(self,List,NumDict):
		super(WeekBaseGetClass, self).__init__()
		self.List = List
		self.NumDict = NumDict

	def _formatGetNumber(self,string,number,strIndexList):
		pass

	def _getNumber(self,string,keyWord):
		pass

	def get(self):
		global timeString
		inList = False
		keyWord = None
		number = None
		for item in self.List:
			if item in timeString:
				inList = True
				keyWord = item
		if inList:			
			number = self._getNumber(timeString,keyWord)
		return (keyWord,number)	

class GetWeekNum(WeekBaseGetClass):
	"""获取周数的类"""
	def __init__(self):
		self.weekNumList = ['星期','周']
		self.weekNumNumDict = {
			'上上个':-2,'下下个':2,'上个':-1,'下个':1,'上上':-2,'下下':2,'这个':0,'上':-1,'下':1,'这':0,'今':0
		}
		super(GetWeekNum, self).__init__(self.weekNumList,self.weekNumNumDict)

	def _getNumber(self,string,keyWord):
		number = None
		string = string.split(keyWord,1)[0] + keyWord
		try:
			getNumber = re.findall('\d+',string,re.S)[-1]
			number = self._formatGetNumber(string,getNumber)
		except IndexError as indexError:
			inList = False
			for item in self.NumDict.keys():
				if item in string:
					inList = True
					break
			if inList == True:					#如果numList中没有传入的字符串，说明没有定义到该字段，很有可能是异常情况
				for item in self.NumDict:
					if item in string:
						number = self.NumDict.get(item)
			else:
				number = None
		except Exception as e:
			raise e
		return number


	def _formatGetNumber(self,string,number):
		strIndexList=[8,10]
		if '前' not in string and '后' not in string and '上' not in string and '下' not in string:
			yearNow = now[strIndexList[0]:strIndexList[1]]
			retNumber = int(number) - int(yearNow)
		else:
			if '前' in string or '上' in string:
				retNumber = int('-'+ str(number))
			elif '后' in string or '下' in string:
				retNumber = int(number)
		return retNumber

class GetWeek(WeekBaseGetClass):
	"""
		获取星期的类
		这个类与其他类不太相同，处理因为不用对取出数值进行格式化，并且在关键字后面必须为数字才是合法的星期表示方式，
		所以只需要取出关键字后的数值即可
	"""
	def __init__(self):
		self.weekList = ['星期','周']
		self.weekNumList = {
			'星期1':1,'星期2':2,'星期3':3,'星期4':4,'星期5':5,'星期6':6,'星期天':7,'星期日':7,
			'周1':1,'周2':2,'周3':3,'周4':4,'周5':5,'周6':6,'周天':7,'周日':7
		}
		super(GetWeek, self).__init__(self.weekList,self.weekNumList)

	def _formatGetNumber(self,string):
		global timeString
		inList = False
		for item in self.NumDict.keys():
			if item in string:
				inList = True
				break
		if inList == True:					#如果numList中没有传入的字符串，说明没有定义到该字段，很有可能是异常情况
			for item in self.NumDict:
				if item in string:
					number = self.NumDict.get(item)			#取出对应的星期值，然后修改全局变量timeString的值
					keyWordIndex = string.find(item,0)
					keyWordLength = len(item)
					timeString = timeString[keyWordIndex+keyWordLength:]
		else:
			number = None
		return number

	def _getNumber(self,string,keyWord):
		global timeString
		number = None
		keyWordLength = len(keyWord)
		try:
			index = string.find(keyWord,0)
			if index != -1:
				index += keyWordLength + 1
				string = string[:index]
				number = re.findall('\d+',string,re.S)[0]
				timeString = timeString[index:]
		except IndexError as indexError:
			number = self._formatGetNumber(timeString)
		except Exception as e:
			raise e
		return number



class GetAmPm(object):
	"""获取上下午的类"""
	def __init__(self):
		super(GetAmPm, self).__init__()
		self.ampmDict = {
			'上午':0,'凌晨':0,'早上':0,
			'中午':1,'下午':1,'傍晚':1,'晚上':1,'深夜':1,
		}

	def get(self):
		global timeString
		keyWord = None
		number = None
		for item in self.ampmDict:
			if item in timeString:
				keyWord = item
				number = self.ampmDict.get(item)
				break
		if keyWord:
			keyWordIndex = timeString.find(keyWord,0)
			keyWordLength = len(keyWord)
			timeString = timeString[keyWordIndex + keyWordLength:]
		return (keyWord,number)
		

		
class GetHour(DateTimeBaseClass):
	"""获取时的类"""
	def __init__(self):
		self.hourList = ['小时之前','小时之后','点之前','点之后','小时前','小时后','小时','时候','点整','时整','点前','点后','点','时']
		self.hourNumDict = {
			'上个小时':-1,'下个小时':1,
			'半个小时':0.5,'半小时':0.5,
			'时候':0,'时':0
		}
		super(GetHour, self).__init__(self.hourList,self.hourNumDict)

	def _formatGetNumber(self,keyWord,string,number):
		return super()._formatGetNumber(keyWord,string,number,[13,15])
		
class GetMinute(DateTimeBaseClass):
	"""获取分的类"""
	def __init__(self):
		self.minuteList = ['分钟之前','分钟之后','分钟前','分钟后','分之前','分之后','分前','分后','分钟','分','半']
		self.minuteNumDict = {
			'上分钟':-1,'下分钟':1,
			'半':0.5
		}
		super(GetMinute, self).__init__(self.minuteList,self.minuteNumDict)

	def _formatGetNumber(self,keyWord,string,number):
		return super()._formatGetNumber(keyWord,string,number,[15,17])
		
class GetSecond(DateTimeBaseClass):
	"""获取秒的类"""
	def __init__(self):
		self.secondList = ['秒钟之前','秒钟之后','秒之前','秒之后','秒钟后','秒后']
		self.secondNumDict = {
			'上个小时':-1,'下个小时':1
		}
		super(GetSecond, self).__init__(self.secondList,self.secondNumDict)

	def _formatGetNumber(self,keyWord,string,number):
		return super()._formatGetNumber(keyWord,string,number,[17,19])


class GetNow(object):
	"""获取的是当前的时间"""
	def __init__(self):
		super(GetNow, self).__init__()
		self.nowList = ['当前时间','现在时间','这个时候','这时候','现在','这时']

	def get(self):
		"""如果字符串包含类属性nowList包含的关键词，则获取此时此刻的时间"""
		pass