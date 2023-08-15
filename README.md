
# MaPool


接码服务器，采集各个手机验证码短信接码平台的免费号码，自定义插拔 路由和处理器，低耦合的接码服务器~

## 使用

* 依赖: `pip install -r requirements.txt`
* 运行: `python main.py`

 
 
 ## 示例
 
 ### 1.使用内置的接码器获取可用手机号码
 通过`python main.py`运行服务器,而后：
 ```python
import requests
api = 'http://127.0.0.1:8899/mianfeisms/phone?area=cn&page=1&pages=10'
data = requests.get(api)
```
返回数据：
```json
{
	"success": 0,
	"data": {
		"code": "86",
		"area": "China",
		"phones": [
      "+8618301976717", "+8613998249844", "+8615134463117", "+8618142665405", "+8615866624279",
      "+8613734534942", "+8615879140693", "+8618276058544", "+8613594263015", "+8615993039983", 
      "+8615259322759", "+8618225465406", "+8615476439183", "+8613513827220", "+8615938883624"
    ],
		"total": 90
	}
}
```      

### 2.使用内置服务器查询手机号码 +853 68436533中 “美团网” 相关的长度为4的验证码信息

 通过`python index.py`运行服务器,而后：
 ```python
import requests
api = 'http://127.0.0.1:8899/mianfeisms/fetch?phone=15938883624&name_pattern=平安口袋银行&code_length=4'
data = requests.get(api)
```

返回数据：
```json
{
  "success": 0, 
  "data": [
    {
      "from": "301510063271", 
      "message": "\u3010\u5e73\u5b89\u53e3\u888b\u94f6\u884c\u3011\u60a8\u767b\u5f55\u7cfb\u7edf\u7684\u52a8\u6001\u7801\u4e3a\uff1a7848\uff0c\u52a8\u6001\u7801\u6709\u6548\u65f6\u95f4\u4e3a5\u5206\u949f\uff0c\u8bf7\u6ce8\u610f\u4fdd\u5bc6\u3002", 
      "time": "2023-08-14 19:13:49", 
      "code": ["7848"]
    }
  ]
}
```

## 自定义
