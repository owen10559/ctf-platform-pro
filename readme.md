

# 接口说明
## 获取training
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

## 修改training
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

## 获取training信息
### URI说明
**GET** /trainings
|参数名|必填|说明
|:----:|:----:|:----:
|training_name|否|training的名称

返回指定training的详细信息。若training_name为空，则返回所有training的名称。
|参数名|类型|说明
|:----:|:----:|:----: 
| training_id | string | training的id
### DEMO
**GET** /trainings

**RESPONSE**
```
{

}
```