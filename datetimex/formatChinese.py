class FormatChinese(object):
    """
    这个类用作转换传入的中文为数字
    部分核心代码引用自互联网，由于时间问题，已经找不到原作者
    版权归属于原作者，这部分代码经过部分加工或修改，如若存在侵权问题，请联系我
    """
    def __init__(self):
        super(FormatChinese, self).__init__()
        self.common_used_numerals_tmp = {'零': 0 , '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                                    '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
        self.common_used_numerals = {}
        for key in self.common_used_numerals_tmp:
            self.common_used_numerals[key] = self.common_used_numerals_tmp[key]
        self.num_str_start_symbol = ['零','一', '二', '两', '三', '四', '五', '六', '七', '八', '九','十']
        self.more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']

    def __chinese2digits(self,uchars_chinese):
        total = 0
        string = ''
        r = 1  # 单位：个十百千...
        for i in range(len(uchars_chinese) - 1, -1, -1):
            val = self.common_used_numerals.get(uchars_chinese[i])
            if val >= 10 and i == 0:                  # 应对 十三 十四 十*之类
                if val > r:
                    r = val
                    total = total + val
                else:
                    r = r * val
            elif val >= 10:
                if val > r:
                    r = val
                else:
                    r = r * val
            else:
                if len(uchars_chinese) < 4:           ##这里处理传入值长度大于4问题，大于等于四一般应该正常读取而不作运算,而长度小于4应该作运算处理
                    total = total + r * val           #例如年份：一九九七，该返回1997而并非26，一二三四五六七八九十一九九七年，该返回123456789而并非450
                else:
                    string = str(val) + string
                    total = int(string)
        return total

    def __changeChineseNumToArab(self,oriStr):
        lenStr = len(oriStr);
        aProStr = ''
        if lenStr == 0:
            return aProStr;
     
        hasNumStart = False;
        numberStr = ''
        for idx in range(lenStr):
            if oriStr[idx] in self.num_str_start_symbol:
                if not hasNumStart:
                    hasNumStart = True;
     
                numberStr += oriStr[idx]
            else:
                if hasNumStart:
                    if oriStr[idx] in self.more_num_str_symbol:
                        numberStr += oriStr[idx]
                        continue
                    else:
                        numResult = str(self.__chinese2digits(numberStr))
                        numberStr = ''
                        hasNumStart = False;
                        aProStr += numResult
     
                aProStr += oriStr[idx]
                pass
     
        if len(numberStr) > 0:
            resultNum = self.__chinese2digits(numberStr)
            aProStr += str(resultNum)
        return aProStr

    def format(self,ChineseStr):
        """类入口，传入要转换的中文，返回转换后的字符串，具体实现方法不暴露给外部，只给外部提供一个format方法"""
        return self.__changeChineseNumToArab(ChineseStr)