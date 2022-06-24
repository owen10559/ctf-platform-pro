

# api说明
## 启动一个training
### URI说明
**GET** /\<username\>/\<training_name\>

\<username\>：用户名

\<training_name\>：training的名称

为指定用户启动某个training，返回该training的id。若用户已创建该training，则也返回对应的id。

### 状态码和返回值
**200：** 启动成功（或已启动）
|参数名|类型|说明
|:----:|:----:|:----: 
| training_id | string | training的id


**400：** 请求参数错误

无返回值

## 停止一个training
### URI说明
**DELETE** /\<username\>/\<training_name\>

\<username\>：用户名

\<training_name\>：training的名称

为指定用户停止某个training，返回该training的id。若该training已停止，则也返回对应的id。