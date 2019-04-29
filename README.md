# 数据库结构

## `user`表

`userid,username,password,token,personsay`

数据库储存格式：

|   字段名    |                值                |
| :---------: | :------------------------------: |
|   userid    |               123                |
|  username   |             Z3Vlc3Q=             |
|  password   |             MTIzNDU2             |
|    token    | e6c43826c85c78644a6c97ec6205ab0b |
|  personsay  |     6L+Z5piv5Liq5oCn562+5ZCN     |
| userarticle |           [12,13,132]            |
| usercomment |            [11,25,33]            |

相关字段解释：

| 字段名      | 解释                                                         |
| ----------- | ------------------------------------------------------------ |
| token       | 用户token鉴权，生成格式：`md5(base64(username|password)) `   |
| personsay   | 个性签名字段，6L+Z5piv5Liq5oCn562+5ZCN，即base64("这是个性签名") |
| userarticle | 用户发表的文章id，`[12,13,132]`                              |
| usercomment | 用户发表的评论id，`[11,25,33]`                               |

> token生成伪代码
>
> `token=md5(base64.b64encode（"{username}|{password}".format(username="Z3Vlc3Q=",password="MTIzNDU2")))`

## `article` 表

`articleid,articletitle,articleauthor，articleauthorid,articlecontent,articletimestamp，commentid`

数据库储存格式

|      字段名      |            值            |
| :--------------: | :----------------------: |
|    articleid     |           135            |
|   articletitle   | 6L+Z5piv5paH56ug5qCH6aKY |
|  articleauthor   |         Z3Vlc3Q=         |
| articleauthorid  |           123            |
|  articlecontent  |   5YaF5a655Zyo6L+Z6YeM   |
| articletimestamp |        1556464204        |
|    commentid     |        [12,62,32]        |

相关字段解释：

| 字段名           | 解释               |
| ---------------- | ------------------ |
| articleauthorid  | 文章发表者的userid |
| articletimestamp | 发表文章时的时间戳 |
| commentid        | 文章的评论id       |

## `comment`表

`commentid,commentauthor,commentauthorid,commentcontent,commenttimestamp`

数据库储存格式

|      字段名      |          值          |
| :--------------: | :------------------: |
|    commentid     |          23          |
|  commentauthor   |       Z3Vlc3Q=       |
| commentauthorid  |         123          |
|  commentcontent  | 5YaF5a655Zyo6L+Z6YeM |
| commenttimestamp |      1556464204      |

相关字段解释：

| 字段名          | 解释               |
| --------------- | ------------------ |
| commentauthorid | 评论发表者的userid |

# 登录注册

## 登录：

### **路由：`/api/login`**

`post`数据

```json
{
    "username":"Z3Vlc3Q=",
    "password": "MTIzNDU2"
}
```

username和password我会用base64传输`Z3Vlc3Q=` 即为用户guest，`MTIzNDU2` 为123456

数据库也是base64储存

登录成功:

```json
{
	"success":1,
    "token":"e6c43826c85c78644a6c97ec6205ab0b",
    "msg":"登录成功～"
}
```

登录失败:

```json
{
	"success":0,
    "msg":"登录失败～"
}
```



## 注册：

### **路由 : `/api/register`**

`post`数据

```json
{
    "username":"Z3Vlc3Q=",
    "password": "MTIzNDU2"
}
```

注册成功：

```json
{
	"success":1,
    "token":"e6c43826c85c78644a6c97ec6205ab0b",
    "msg":"注册成功～"
}
```

用户名已占用：

```json
{
	"success":0,
    "msg":"用户名已占用～"
}
```

其他原因注册失败：

```json
{
	"success":0,
    "msg":"注册失败～"
}
```



# 文章

## 查询文章：

### 路由：`/api/article/search`

`post`数据:

```json
{
    "articleidarray":[11,23,42],
    "token":"e6c43826c85c78644a6c97ec6205ab0b"
}
```

返回值:

```json
{
    "success":1,
    "data":[{
    	"articleid" : "11",
    	"articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   		"articleauthor":"Z3Vlc3Q=",
        "articleauthorid":"123",
   		"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   		"articletimestamp":"1556464204",
   		"commentid":"[12,62,32]"
    },{
    	"articleid" : "23",
    	"articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   		"articleauthor":"Z3Vlc3Q=",
        "articleauthorid":"123",
   		"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   		"articletimestamp":"1556464204",
   		"commentid":"[12,62,32]"
    },{
    	"articleid" : "42",
    	"articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   		"articleauthor":"Z3Vlc3Q=",
        "articleauthorid":"123",
   		"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   		"articletimestamp":"1556464204",
   		"commentid":"[12,62,32]"
    }]
}
```

## 首页文章分页显示：

### 路由：`/api/article/index`

每页3篇文章：

后端使用`limit`进行分页,使用时间降序查询，

```sqlite
(select * from article desc articletimestamp limit pagenum*3,pagenum*3+3),pagenum
```

实现分页查询功能

`post`发送请求：

```json
{
    "pagenum":0,
    "token":"e6c43826c85c78644a6c97ec6205ab0b"
}
```

返回值：

```json
{
    "success":1,
    "data":[{
    	"articleid" : "11",
    	"articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   		"articleauthor":"Z3Vlc3Q=",
   		"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   		"articletimestamp":"1556464204",
   		"commentid":"[12,62,32]"
    },{
    	"articleid" : "23",
    	"articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   		"articleauthor":"Z3Vlc3Q=",
   		"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   		"articletimestamp":"1556464204",
   		"commentid":"[12,62,32]"
    },{
    	"articleid" : "42",
    	"articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   		"articleauthor":"Z3Vlc3Q=",
   		"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   		"articletimestamp":"1556464204",
   		"commentid":"[12,62,32]"
    }]
}
```

## 发送文章

### 路由：`/api/article/add`

`post`发送请求：

```json
{
    "articletitle":"6L+Z5piv5paH56ug5qCH6aKY",
   	"articleauthor":"Z3Vlc3Q=",
    "articleauthorid":"123",
   	"articlecontent":"5YaF5a655Zyo6L+Z6YeM",
   	"articletimestamp":"1556464204",
    "token":"e6c43826c85c78644a6c97ec6205ab0b"
}
```

添加成功：

```json
{
	"success":1,
    "msg":"添加成功"
}
```

添加失败：

```json
{
	"success":0,
    "msg":"添加失败"
}
```



# 评论

## 评论查询

### 路由:`/api/comment/search`

`post`发送请求：

```json
{
    "commentidarrary":[11,12,33],
    "token":"e6c43826c85c78644a6c97ec6205ab0b"
}
```

返回值：

```json
{
    "success":1,
    "data":[{
    	"commentid" : "11",
   		"commentauthor":"Z3Vlc3Q=",
        "commentauthorid":"123",
   		"commentcontent":"5YaF5a655Zyo6L+Z6YeM",
   		"commenttimestamp":"1556464204"
    },{
    	"commentid" : "11",
   		"commentauthor":"Z3Vlc3Q=",
        "commentauthorid":"123",
   		"commentcontent":"5YaF5a655Zyo6L+Z6YeM",
   		"commenttimestamp":"1556464204"
    },{
    	"commentid" : "11",
   		"commentauthor":"Z3Vlc3Q=",
        "commentauthorid":"123",
   		"commentcontent":"5YaF5a655Zyo6L+Z6YeM",
   		"commenttimestamp":"1556464204"
    }]
}
```

## 发送评论

### 路由：`/api/comment/add`

`post`发送请求：

```json
{
   	"commentauthor":"Z3Vlc3Q=",
    "commentauthorid":"123",
   	"commentcontent":"5YaF5a655Zyo6L+Z6YeM",
   	"commenttimestamp":"1556464204",
    "token":"e6c43826c85c78644a6c97ec6205ab0b"
}
```

添加成功：

```json
{
	"success":1,
    "msg":"添加成功"
}
```

添加失败：

```json
{
	"success":0,
    "msg":"添加失败"
}
```



# 用户个人中心

## 修改密码/个性签名：

### 路由:`/api/user/change`

```json
{
    "token":"e6c43826c85c78644a6c97ec6205ab0b",
	"oldpassword":"MTIzNDU2",
    "newpassword":"OTYzLjEyMw==",
    "personsay":"6L+Z5piv5Liq5oCn562+5ZCN"
}
```

成功修改/未做修改：

```json
{
    "success":1,
    "token":"e6c43826c85c78644a6c97ec6205ab0b",
    "msg":"成功修改"
}
```

修改失败/原密码错误：

```
{
    "success":1,
    "token":"e6c43826c85c78644a6c97ec6205ab0b",
    "msg":"修改失败/原密码错误"
}
```

**oldpassword或newpassword任意一个参数为空`""` 则认为不修改密码，只更改签名**

## 查询个人信息

发送请求：

```json
{
    "userid":"132",
    "token":"e6c43826c85c78644a6c97ec6205ab0b"
}
```

返回值：

```json
{
    "userid":"132",
	"username":"Z3Vlc3Q=",
    "userarticle":[11,335,520],
    "usercomment":[20,52,95]
}
```



# 功能实现样例

伪代码

```python
@app.route("/api/article/search",method="POST")
def article():
	reqdata=json.get()
    if checklogin(reqdata["token"]): 
		returndata={"success":1,"data":[]}
		for i in reqdata["articleidarray"]:
			sql=function("select * from article where articleid= ?",i)
			tmpdata=dict(sqldata)
			returndata["data"].append(tmpdata)
		return jsonify(returndata)
    else:
        return jsonify({"success":0,"msg":"请登录"})
```

