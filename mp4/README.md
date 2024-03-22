# MP4 - Lambda

## 部署
### 前置条件
具备 AWS 账户，且已经在console中使用MediaConvert进行过转码操作

### 部署代码
1. 进入Lambda控制台：https://console.aws.amazon.com/lambda/home

2. 点击"Create function"， 默认"Author from scratch"，"Function Name" 填 "mediaconvert-mp4", "Runtime"选择"Python 3.12"，其它选项保持默认值，点击"创建"。

3. 使用lambda_function.py中的代码替换Lambda编辑器中的代码（复制粘贴，全量替换即可）。

4. 保存，并点击页面“Deploy”按钮进行部署。

### 调整Lambda配置
5. 紧接上一步，在Lambda页面点击"Configuration"，点击左侧"General configuration"，将"Timeout"超时时间设置为1分钟，保存。

6. 点击左侧"Permissions"，点击role链接，跳转至IAM页面，为角色添加"AWSElementalMediaConvertFullAccess" Policy。

7. 回到Lambda->Configuration页面，点击左侧"Environment variables"，添加环境变量，key为"MEDIACONVERT_ROLE", value为MediaConvert中转码时使用的Role的ARN。

## 使用Lambda
需使用AWS SDK 中的Lamdba invoke方法调用Lamdba函数，

参数：

`video_source_file`：输入文件s3路径

`destination_path`：输出文件s3路径(最后以`/`结尾)

Python Demo:
```
import boto3
import json

lambda_client = boto3.client('lambda')

data = {
    'video_source_file': "s3://YOUR_BUCKET/source_file.mp4",
    'destination_path': "s3://allenzh-public/videos/mp4/3/"
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