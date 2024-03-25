# 通用转码 - Lambda

## 部署
### 前置条件
具备 AWS 账户，且已经在console中使用MediaConvert进行过转码操作

### 部署代码
1. 进入Lambda控制台：https://console.aws.amazon.com/lambda/home

2. 点击"Create function"， 默认"Author from scratch"，"Function Name" 填 "mediaconvert-general", "Runtime"选择"Python 3.12"，其它选项保持默认值，点击"创建"。

3. 使用lambda_function.py中的代码替换Lambda编辑器中的代码（复制粘贴，全量替换即可）。

4. 在编辑器中新建文件，命名可自定义（全英文），以`.json`后缀保存，例如：`mp4-with-cover.json`，将控制台导出的json内容拷贝入文件中。

5. 保存，并点击页面“Deploy”按钮进行部署。

### 调整Lambda配置
5. 紧接上一步，在Lambda页面点击"Configuration"，点击左侧"General configuration"，将"Timeout"超时时间设置为1分钟，保存。

6. 点击左侧"Permissions"，点击role链接，跳转至IAM页面，为角色添加"AWSElementalMediaConvertFullAccess" Policy。

## 使用Lambda
需使用AWS SDK 中的Lamdba invoke方法调用Lamdba函数，

参数：

`video_source_file`：输入文件s3路径

`destination_path`：输出文件s3路径(最后以`/`结尾)

`setting`：setting文件名（不加后缀），例如：`mp4-with-cover`

Python Demo:
```
import boto3
import json

lambda_client = boto3.client('lambda')

data = {
    'video_source_file': "s3://YOUR_BUCKET/source_file.mp4",
    'destination_path': "s3://YOUR_BUCKET/videos/mp4/3/",
    'setting': 'mp4-with-cover'
}

response = lambda_client.invoke(
    FunctionName='mediaconvert_create_job',
    Payload=json.dumps(data)
)
payload = response['Payload'].read().decode("utf-8")

lamdba_res_payload = json.loads(payload)
```

Java Demo: 

https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/javav2/example_code/lambda