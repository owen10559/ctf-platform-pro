

# 接口说明
## 获取 training
### 接口说明
为指定用户启动某个training，返回该training的信息。若用户已创建该training，则也返回对应信息。
|URI|方法
|:----:|:----:
|/\<username\>/\<training_name\>|GET

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:
|username|是|用户名
|training_name|是|training的名称

### 状态码和返回值
**200**
|参数名|类型|说明
|:----:|:----:|:----: 
| training_id | string | training的id
| status | number | training的状态（1表示正在运行，0表示已停止）
| ttl | number | training的剩余时间，单位为秒

### DEMO
**GET** /user1/training1

**RESPONSE**
```json
{
    "training_id": "abc12345",
    "status": 1,
    "ttl": 3600
}
```

## 修改 training
### 接口说明
为指定用户修改某个training的信息（例如停止某个training等），返回修改后training的信息。
|URI|方法
|:----:|:----:
|/\<username\>/\<training_name\>|PUT

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:
|username|是|用户名
|training_name|是|training的名称

### 请求体参数
|参数名|必填|类型|说明
|:----:|:----:|:----:|:----:
| status |否| number | training的状态（1表示正在运行，0表示已停止）

### 状态码和返回值
**200**
|参数名|类型|说明
|:----:|:----:|:----: 
| training_id | string | training的id
| status | number | training的状态（1表示正在运行，0表示已停止）
| ttl | number | training的剩余时间，单位为秒

### DEMO
**PUT** /user1/training1

**REQUEST**
```json
{
    "status": 0
}
```

**RESPONSE**
```json
{
    "training_id": "abc12345",
    "status": 0,
    "ttl": 3500
}
```

## 删除 training
### 接口说明
为指定用户删除某个training，返回空。
|URI|方法
|:----:|:----:
|/\<username\>/\<training_name\>|DELETE

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:
|username|是|用户名
|training_name|是|training的名称

### 状态码和返回值
**200**
无返回值。

### DEMO
**DELETE** /user1/training1

**RESPONSE**
```
```

## 获取 training 信息
### 接口说明
返回指定training的信息。若training_name为空，则返回所有training的名称。
|URI|方法
|:----:|:----:
|/trainings|GET

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:
|training_name|否|training的名称

### 状态码和返回值
**200**
|参数名|类型|说明
|:----:|:----:|:----: 
| trainings | array | 所有training的名称的集合（当training_name为空时有效）
| training_name | string | training的名称
| description | string | training的描述（参考对应config.json文件的description字段）
| hint | string | training的提示（参考对应config.json文件的hint字段）

### DEMO
**GET** /trainings

**RESPONSE**
```json
{
    "trainings":["training1", "training2"]
}
```

**GET** /trainings?training_name=training1

**RESPONSE**
```json
{
    "training_name": "training1",
    "description": "here is description of training1.",
    "hint": "here is hint of training1."
}
```

## 验证 flag
### 接口说明
验证获得的flag是否正确
|URI|方法
|:----:|:----:
|/flags/\<training_name>/\<flag>|GET

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:
|training_name|是|training的名称
|flag|是|获得的flag

### 状态码和返回值
200
|参数名|类型|说明
|:----:|:----:|:----: 
|result|number|验证结果，1表示正确，0表示错误

### DEMO
**GET** /flags/training1/flag\{flag_of_training1}

**RESPONSE**
```json
{
    "result": 1
}
```

## training 入口（待定）

### 接口说明

|            URI            | 方法 |
| :-----------------------: | :--: |
| /entrances/\<training_id> | 所有 |

### URI参数

| 参数名 | 必填 | 说明 |
| :----: | :--: | :--: |

### 请求体参数

| 参数名 | 必填 | 类型 | 说明 |
| :----: | :--: | :--: | :--: |

### 状态码和返回值

| 参数名 | 类型 | 说明 |
| :----: | :--: | :--: |

### DEMO


**RESPONSE**

```json

```



---
---
## 接口说明模板
### 接口说明

|URI|方法
|:----:|:----:

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:

### 请求体参数
|参数名|必填|类型|说明
|:----:|:----:|:----:|:----:

### 状态码和返回值

|参数名|类型|说明
|:----:|:----:|:----: 

### DEMO


**RESPONSE**
```json

```

