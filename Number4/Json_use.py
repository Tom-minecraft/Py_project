import json

str = '''
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''
print(type(str))
data = json.loads(str)
print(data)
print(type(data))

# 值得注意的是，JSON 的数据需要用双引号来包围，不能使用单引号。
# 例如，若使用如下形式表示，则会出现错误
import json

str = '''
[{
    'name': 'Bob',
    'gender': 'male',
    'birthday': '1992-10-18'
}]
'''
data = json.loads(str)
#-----> json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 3 column 5 (char 8)


str = '''
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''
with open("data.json", "w",encoding="utf-8") as f:
    f.write(json.dumps(str))

"""--------------------------------------------------------------------------"""


import json

with open('data.json','r', encoding='utf-8') as f:
    str = f.read()

data = json.loads(str)
print(data)
# 注意这里使用的是 load 方法，而不是 loads 方法。前者的参数是一个文件操作对象，后者的参数是一个 JSON 字符串。
# 这两种写法的运行结果也是完全一样的。只不过 load 方法是将整个文件的内容转化为 JSON 对象，而使用 loads 方法可以更灵活地控制要转化的内容。两种方法可以在适当的场景下使用。


"""-----------------------------substantial---------------------------------------------"""
import json

data = [{
    'name': 'Bob',
    'gender': 'male',
    'birthday': '1992-10-18'
}]
with open('data.json', 'w') as file:
    file.write(json.dumps(data, indent=2))


"""-----------------------------substantial(chinese)---------------------------------------------"""

import json

data = [{
    'name': '王伟',
    'gender': '男',
    'birthday': '1992-10-18'
}]
with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2,ensure_ascii=False))