#  datetimex-说明文档

## 简述
	这是一个适用于中文时间字符串格式化的Python库.
	可以实现格式化一些中文带有时间的字符串,格式化后将数字结果返回.
	即：【中文时间】　>　【数字时间】
 
## 环境依赖
	Python 3.x
## 安装
	pip3 install datetimex
## 使用
```
import datetimex

test = datetimex.gettime('明天早上七点半')
test2 = datetimex.gettime('两天前的晚上十一点四十五分')

print(test)
print(test2)

结果如下：

('20181214495PM045543', '20181215496AM073000')
('20181214495PM045543', '20181212493PM114500')

gettime方法返回值为一个元组,其中第一项为当前时间，第二项为格式化后的时间.
两个字符串长度均为19,其中：
1~4位代表年份,5~6位代表月份,7~8位代表日,
9~10位代表周数(一年内所在的第几周),
11位代表星期几(星期天为一周的第一天,为0),
12~13位代表上下午
14~15位代表时，16~17位代表分,18~19位代表秒

上面两句代码得到的结果，表示：
在2018年12月14日,也是该年第49周的星期五的下午四点五十五分四十三秒执行的程序,分别传入“明天早上七点半”和“两天前的晚上十一点四十五分”,
执行结果分别返回的是:
2018年12月15日，也是该年的第49周星期六的早上7点30分，
2018年12月12日，该年的第49周星期三的晚上11点45分
```
## 注意事项
	必须成功安装Python、pip等,并且正确配置环境变量,否则该库可能无法正常工作.
	使用过程中，应当尽可能使用正确的汉语进行传入，这样能更大限度的进行识别其中带有的时间，一些不合法的汉语传入，可能导致无法正常识别，例如：明天后天前天的晚上七点半、今天早上下午晚上三点等，此类汉语为不合法传入，库将无法识别其中带有的时间，为了能尽可能精准的识别出，在传入字符串值时，应尽量合法(符合日常用语)以及尽量简短

## 许可证
	GPL

## 效果图
![](https://github.com/GreenLotusx/DateTimex/blob/master/pic.png)  

