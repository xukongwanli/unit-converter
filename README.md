# unit-converter
#This python library can be used for unit conversions in python programs such as engineering calculations. Currently there is only one main function, feel free to add branches and new functions. To use this function you need to pre-import the re and collections libraries. The usage is as follows:

import u_conv as u
value1=u.conv_u('K','c',273)
value2=u.conv_u('km','m',10)
value3=u.conv_u('lbf/in^2','Pa',10)
value4=u.conv_u('kg*m/s','g*km/min',10)

#If you can't find the base unit you want to convert, you can add it by yourself to the "conversion_table" in the format shown below:
'unit name or abbr':{'factor':the ratio to the base unit,'dimensions':{'base unit type1': number1, 'base unit type2': number2, etc}}

#example:
'm': {'factor': 1.0, 'dimensions': {'L': 1}},
'km': {'factor': 1e3, 'dimensions': {'L': 1}},
'N': {'factor': 1.0, 'dimensions': {'M': 1, 'L': 1, 'T': -2}},
