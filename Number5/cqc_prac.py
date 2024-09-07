import execjs
import json

# 获取 execjs 的运行环境
node = execjs.get()

# 读取并编译 JavaScript 文件内容
with open("cqc_decode.js", 'r', encoding='utf-8') as f:
    cxt = f.read()

js_cxt = node.compile(cxt)

# 定义 item 作为一个 Python 字典，并将其转换为 JSON 字符串
item = {
    "name": "凯文-杜兰特",
    "image": "durant.png",
    "birthday": "1988-09-29",
    "height": "208cm",
    "weight": "108.9KG"
}

# 调用 JavaScript 中的 getToken 函数，并将 item 作为参数传递
result = js_cxt.call("getToken", item)







