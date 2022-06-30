

# 接口说明

## 获取 training 信息

### 接口说明
获取指定用户拥有的某个 training 的信息，并返回。若用户未创建（即未拥有）该 training，则返回空。
|URI|方法
|:----:|:----:
|/\<username\>/\<training_name\>|GET

### URI参数
|参数名|必填|说明|
|:----:|:----:|:----:|
|username|是|用户名|
|training_name|是|training的名称|

### 状态码和返回值
**200**

|参数名|类型|说明|
|:----:|:----:|:----: |
| training_id | string | training的id|
| status | number | training的状态（1表示正在运行，0表示已停止）|
| ttl | number | training的剩余存活时间，单位为秒 |

**404**

无返回值

### DEMO

**REQUEST**

GET /user1/training1

**RESPONSE**

200

```json
{
    "training_id": "abc12345",
    "status": 1,
    "ttl": 3599
}
```

**REQUEST**

GET /user1/training2

**RESPONSE**

404

```json

```

## 创建 training

### 接口说明

为指定用户创建并启动某个 training，返回该 training 的信息。若用户已拥有该 training，则也返回对应信息。

|               URI               | 方法 |
| :-----------------------------: | :--: |
| /\<username\>/\<training_name\> | POST |

### URI参数

|    参数名     | 必填 |      说明       |
| :-----------: | :--: | :-------------: |
|   username    |  是  |     用户名      |
| training_name |  是  | training 的名称 |

### 状态码和返回值

**201**

|   参数名    |  类型  |                     说明                     |
| :---------: | :----: | :------------------------------------------: |
| training_id | string |                 training的id                 |
|   status    | number | training的状态（1表示正在运行，0表示已停止） |
|     ttl     | number |       training的剩余存活时间，单位为秒       |

**400**

|   参数名    |  类型  |                     说明                     |
| :---------: | :----: | :------------------------------------------: |
| training_id | string |                 training的id                 |
|   status    | number | training的状态（1表示正在运行，0表示已停止） |
|     ttl     | number |       training的剩余存活时间，单位为秒       |

### DEMO

**REQUEST**

POST /user1/training2

**RESPONSE**

201

```json
{
    "training_id": "efg45678",
    "status": 1,
    "ttl": 3600
}
```

**REQUEST**

POST /user1/training1

**RESPONSE**

400

```json
{
    "training_id": "abc12345",
    "status": 1,
    "ttl": 3599
}
```

## 修改 training 信息

### 接口说明
修改指定用户拥有的某个 training 的信息（例如 status），返回修改后 training 的信息。若用户未创建（即未拥有）该 training，则返回空。
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
**201**

|参数名|类型|说明
|:----:|:----:|:----: 
| training_id | string | training的id
| status | number | training的状态（1表示正在运行，0表示已停止）
| ttl | number | training的剩余时间，单位为秒

**404**

无返回值

### DEMO

**REQUEST**

PUT /user1/training1

```json
{
    "status": 0
}
```

**RESPONSE**

201

```json
{
    "training_id": "abc12345",
    "status": 0,
    "ttl": 3500
}
```

**REQUEST**

PUT /user1/training3

```json
{
    "status": 0
}
```

**RESPONSE**

404

```json

```

## 删除 training

### 接口说明
为指定用户删除某个training，返回空。若用户未创建（即未拥有）该 training，也返回空。
|URI|方法
|:----:|:----:
|/\<username\>/\<training_name\>|DELETE

### URI参数
|参数名|必填|说明
|:----:|:----:|:----:
|username|是|用户名
|training_name|是|training的名称

### 状态码和返回值
**204**
无返回值。

**404**
无返回值。

### DEMO

**REQUEST**

DELETE /user1/training1

**RESPONSE**

204

```
```

**REQUEST**

DELETE /user1/training3

**RESPONSE**

404

```

```

## 获取 training 说明

### 接口说明
返回指定 training 的说明。若 training_name 为空，则返回所有 training 的名称。若 training 不存在，则返回空。
|URI|方法|
|:----:|:----:|
|/trainings/\<training_name\>|GET|

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

**404**

无返回值。

### DEMO

**REQUEST**

GET /trainings

**RESPONSE**

200

```json
{
    "trainings":["training1", "training2"]
}
```

**REQUEST**

GET /trainings/training1

**RESPONSE**

200

```json
{
    "training_name": "training1",
    "description": "here is description of training1.",
    "hint": "here is hint of training1."
}
```

**REQUEST**

GET /trainings/training3

**RESPONSE**

404

```json

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
**200**

|参数名|类型|说明
|:----:|:----:|:----: 
|result|number|验证结果，1表示正确，0表示错误

### DEMO

**REQUEST**

GET /flags/training1/flag\{flag_of_training1}

**RESPONSE**

200

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

