import execjs
import json

item = {
    "name": "凯文-杜兰特",
    "image": "durant.png",
    "birthday": "1988-09-29",
    "height": "208cm",
    "weight": "108.9KG"
}

file = "cqc_original.js"
node = execjs.get()
ctx = node.compile(open(file,encoding='utf-8').read())
Py_item = json.dumps(item,ensure_ascii=False) #Py_item是python的str
print(Py_item)
js = f"getToken({Py_item})"
print(js)
# ----------------js要在python中声明--------------------
result = ctx.eval(js) #eval参数接受str:js表达式
print(result)