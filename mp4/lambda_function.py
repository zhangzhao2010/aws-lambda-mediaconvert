import boto3
import os

def lambda_handler(event, context):
    client = boto3.client('mediaconvert')

    # 视频原文件路径
    video_source_file = event.get('video_source_file', '')

    # 输出S3路径
    destination_path = event.get('destination_path', '')

    if video_source_file == '' or destination_path == '':
        return {
            'error_no': -1,
            'error_msg': 'invalid parameters'
        }

    # mediaconvert 默认角色
    role = os.environ['MEDIACONVERT_ROLE']
    if role == '':
        return {
            'error_no': -1,
            'error_msg': 'invalid role'
        }

    settings = {
        "TimecodeConfig": {
            "Source": "ZEROBASED"
        },
        "OutputGroups": [
            {
                "CustomName": "mp4",
                "Name": "File Group",
                "Outputs": [
                    {
                        "ContainerSettings": {
                            "Container": "MP4",
                            "Mp4Settings": {}
                        },
                        "VideoDescription": {
                            "CodecSettings": {
                                "Codec": "H_264",
                                "H264Settings": {
                                    "MaxBitrate": 6000000,
                                    "RateControlMode": "QVBR",
                                    "SceneChangeDetect": "TRANSITION_DETECTION"
                                }
                            }
                        },
                        "AudioDescriptions": [
                            {
                                "CodecSettings": {
                                    "Codec": "AAC",
                                    "AacSettings": {
                                        "Bitrate": 96000,
                                        "CodingMode": "CODING_MODE_2_0",
                                        "SampleRate": 48000
                                    }
                                }
                            }
                        ]
                    }
                ],
                "OutputGroupSettings": {
                    "Type": "FILE_GROUP_SETTINGS",
                    "FileGroupSettings": {
                        "Destination": destination_path,
                        "DestinationSettings": {
                            "S3Settings": {
                                "StorageClass": "STANDARD"
                            }
                        }
                    }
                }
            }
        ],
        "Inputs": [
            {
                "AudioSelectors": {
                    "Audio Selector 1": {
                        "DefaultSelection": "DEFAULT"
                    }
                },
                "VideoSelector": {},
                "TimecodeSource": "ZEROBASED",
                "FileInput": video_source_file
            }
        ]
    }

    # 创建任务
    response = client.create_job(
        AccelerationSettings={
            'Mode': 'DISABLED'
        },
        Role=role,
        Settings=settings
    )

    del response['Job']['CreatedAt']
    del response['Job']['Timing']
    print(response)

    return {
        'error_no': 0,
        'error_msg': '',
        'data': response
    }
