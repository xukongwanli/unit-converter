# unit-converter
#This Python library can be used for unit conversions in Python programs such as engineering calculations. Currently, there is only one main function, feel free to add branches and new functions. To use this function you need to pre-download the re and collections libraries. The usage is as follows:

#这个 Python 库可用于 Python 程序中的单位转换，如工程计算。目前只有一个主函数，欢迎添加分支和新函数。要使用该函数，需要预先下载好 re 和 collections 库。用法如下：

import u_conv as u

value1=u.conv_u('K','C',273)

value2=u.conv_u('km','m',10)

value3=u.conv_u('lbf/in^2','Pa',10)

value4=u.conv_u('kg*m/s','g*km/min',10)

#If you can't find the base unit you want to convert, you can add it by yourself to the "conversion_table" in the format shown below:

#如果找不到要转换的基本单位，可以按如下所示格式将其添加到 “conversion_table”中：

'unit name or abbr':{'factor':the ratio to the base unit,'dimensions':{'base unit type1': number1, 'base unit type2': number2, etc}}

#example:

'm': {'factor': 1.0, 'dimensions': {'L': 1}},

'km': {'factor': 1e3, 'dimensions': {'L': 1}},

'N': {'factor': 1.0, 'dimensions': {'M': 1, 'L': 1, 'T': -2}},
