# -*- coding: utf-8 -*-
import platform

API_IMAGE_END_POINT = 'http://web.image.myqcloud.com/photos/v1/'
API_IMAGE_END_POINT_V2 = 'http://web.image.myqcloud.com/photos/v2/'
API_VIDEO_END_POINT = 'http://web.video.myqcloud.com/videos/v1/'
APPID = '您的APPID'
SECRET_ID = '您的SECRETID'
SECRET_KEY = '您的SECRETKEY'

image_config = {
    'end_point':API_IMAGE_END_POINT,
    'end_point_v2':API_IMAGE_END_POINT_V2,
    'appid':APPID,
    'secret_id':SECRET_ID,
    'secret_key':SECRET_KEY,
}

video_config = {
    'end_point':API_VIDEO_END_POINT,
    'appid':APPID,
    'secret_id':SECRET_ID,
    'secret_key':SECRET_KEY,
}

def get_app_info(cate='image'):
    if 'image' == cate:
        return image_config
    if 'video' == cate:
        return video_config
    else:
        return ''

def set_app_info(appid=None,secret_id=None,secret_key=None):
    if appid:
        image_config['appid'] = appid
        video_config['appid'] = appid
    if secret_id:
        image_config['secret_id'] = secret_id
        video_config['secret_id'] = secret_id
    if secret_key:
        image_config['secret_key'] = secret_key
        video_config['secret_key'] = secret_key

def get_ua():
    version = "2.1.5"
    return 'QcloudPYTHON/'+version+' ('+platform.platform()+')';


