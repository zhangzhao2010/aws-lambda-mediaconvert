import boto3
import os
import json

def lambda_handler(event, context):
    ###########
    # 1. 获取参数
    ###########
    # 视频原文件路径
    video_source_file = event.get('video_source_file', '')

    # 输出S3路径
    destination_path = event.get('destination_path', '')
    
    # setting file
    setting = event.get('setting', '')
    
    if video_source_file == '' or destination_path == '' or setting == '':
        return {
            'error_no': -1,
            'error_msg': 'invalid parameters.'
        }
    
    setting_json_file = f"./{setting}.json"
    if not os.path.isfile(setting_json_file):
        return {
            'error_no': -1,
            'error_msg': 'invalid setting file path.'
        }
    
    ###########
    # 2. load settings
    ###########
    with open(setting_json_file, 'r') as setting_json:
        settings_full = json.load(setting_json)
    
    ###########
    # 3. update settings
    ###########
    role = settings_full['Role']
    settings = settings_full['Settings']
    settings['Inputs'][0]['FileInput'] = video_source_file
    
    if settings['OutputGroups'][0]['OutputGroupSettings']['Type'] == 'CMAF_GROUP_SETTINGS':
        settings['OutputGroups'][0]['OutputGroupSettings']['CmafGroupSettings']['Destination'] = destination_path
        pass
    elif settings['OutputGroups'][0]['OutputGroupSettings']['Type'] == 'FILE_GROUP_SETTINGS':
        settings['OutputGroups'][0]['OutputGroupSettings']['FileGroupSettings']['Destination'] = destination_path
    
    del(settings['FollowSource'])
    ###########
    # 4. submit job
    ###########
    client = boto3.client('mediaconvert')
    response = client.create_job(
        AccelerationSettings={
            'Mode': 'DISABLED'
        },
        Role=role,
        Settings=settings
    )

    del response['Job']['CreatedAt']
    del response['Job']['Timing']

    return {
        'error_no': 0,
        'error_msg': '',
        'data': response
    }

if __name__ == '__main__':
    res = lambda_handler({
        "video_source_file": "",
        "destination_path": "",
        "setting": "mp4-with-cover"
    }, {})
    
    print(res)
    pass