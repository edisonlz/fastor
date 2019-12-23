# -*- coding: utf-8 -*-

import os.path
import time
import sys
import hashlib
import requests
from tencentyun import conf
from .auth import Auth

class Video(object):

    def __init__(self, appid, secret_id, secret_key):
        self.VIDEO_FILE_NOT_EXISTS = -1
        self.VIDEO_NETWORK_ERROR = -2
        self.VIDEO_PARAMS_ERROR = -3

        self.EXPIRED_SECONDS = 2592000
        self._secret_id,self._secret_key = secret_id,secret_key
        conf.set_app_info(appid, secret_id, secret_key)
		
    """直接上传视频文件
    适用于较小文件，大文件请采用分片上传
    参数:
        filepath:         文件本地路径
        userid:           开发者账号体系下的userid，没有请使用默认值0
        title:            视频标题
        desc:             视频描述
        magic_context:    透传字段，需要开发者设置回调URL,微视频会将信息透传给开发者服务器

    返回值:
        一个json字符串，类似 
		{
			'httpcode': 200,		-----返回的httpcode
			'code': 0,				-----0：成功；非0：失败
			'data': {				-----存放上传结果的json结构
				'url': '',		    -----视频管理url
				'download_url': '', -----视频下载url
				'fileid': ''		-----视频的唯一标识符
				'cover_url': ''		-----视频的封面url，只有设置转码的才有封面url，此key不必定返回
			},
			'message': ''			-----上传失败的错误信息
		}
    """
    def upload(self, filepath, userid='0',title='',desc='',magic_context=''):
        filepath = os.path.abspath(filepath);
        if os.path.exists(filepath):
            expired = int(time.time()) + self.EXPIRED_SECONDS
            url = self.generate_res_url(userid)
            auth = Auth(self._secret_id, self._secret_key)
            sign = auth.app_sign(url, expired)
            size = os.path.getsize(filepath)
            sha1 = hashlib.sha1();
            fp = open(filepath, 'rb')
            sha1.update(fp.read())
            fp.close()

            headers = {
                'Authorization':'QCloud '+sign,
                'User-Agent':conf.get_ua(),
            }

            files = {'FileContent': open(filepath, 'rb'),'Sha':sha1.hexdigest(),'Title':title,'Desc':desc,'MagicContext':magic_context}

            r = {}
            try:
                r = requests.post(url, headers=headers, files=files)
                ret = r.json()
            except Exception as e:
                if r:
                    return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
                else:
                    return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
			
            if 'code' in ret:
                if 0 == ret['code']:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{
                            'url':ret['data']['url'],
                            'download_url':ret['data']['download_url'],
                            'fileid':ret['data']['fileid'],
                            'cover_url':ret['data'].has_key('cover_url') and ret['data']['cover_url'] or '',
                        }
                    }
                else:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{}
                    }
            else:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

        else:
            return {'httpcode':0, 'code':self.VIDEO_FILE_NOT_EXISTS, 'message':'file not exists', 'data':{}}
		
		
    """查询视频状态
    参数:
        fileid:           视频的唯一标识符
        userid:           开发者账号体系下的userid，没有请使用默认值0
    返回值:
        一个json字符串，类似 
		{
			'httpcode': 200,												-----返回的httpcode
			'code': 0,														-----0：成功；非0：失败
			'data': {
				'video_cover_url': '',										-----视频的封面url，只有设置转码的才有封面url
				'video_play_time': 0,										-----视频的播放时间，只有设置转码的才有
				'video_desc': '',											-----视频描述
				'size': '2149433',											-----视频大小，单位byte
				'upload_time': '1434359122',								-----视频上传时间，unix时间戳
				'video_status': '2',										-----视频状态 0-初始化, 1-转码中, 2-转码结束,3-转码失败,4-未审核,5-审核通过,6-审核未通过,7-审核失败
				'video_status_msg': '',									  	-----视频状态 
				'download_url': '',									  	    -----视频下载url
				'sha': '2929d984eac19226dc084a8810c6af319582a8ce',	  	    -----视频sha1值 
				'video_title': '',											-----视频标题
				'fileid': '200679_b22ab0e870a24e59aba5876d06e88280'         -----视频的唯一标识符
			},
			'message': ''													-----上传失败的错误信息
		}
    """
    def stat(self, fileid, userid='0'):
        if not fileid:
            return {'httpcode':0, 'code':self.VIDEO_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid)
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.get(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{
                        'download_url':ret['data']['file_url'],
                        'fileid':ret['data'].has_key('file_fileid') and ret['data']['file_fileid'] or '',
                        'upload_time':ret['data']['file_upload_time'],
                        'size':ret['data']['file_size'],
                        'sha':ret['data']['file_sha'],
                        'video_status':ret['data']['video_status'],
                        'video_status_msg':ret['data']['video_status_msg'],
                        'video_play_time':ret['data'].has_key('video_play_time') and ret['data']['video_play_time'] or 0,
                        'video_title':ret['data'].has_key('video_title') and ret['data']['video_title'] or '',
                        'video_desc':ret['data'].has_key('video_desc') and ret['data']['video_desc'] or '',
                        'video_cover_url':ret['data'].has_key('video_cover_url') and ret['data']['video_cover_url'] or '',
                        },
                    }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{}
                }
        else:
            return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

    """删除视频
    参数:
        fileid:           视频的唯一标识符
        userid:           开发者账号体系下的userid，没有请使用默认值0
    返回值:
        一个json字符串，类似 
		{
			'httpcode': 200,		-----返回的httpcode
			'code': 0,				-----0：成功；非0：失败
			'message': ''	  		-----上传失败的错误信息
		}
    """
    def delete(self, fileid, userid='0'):
        if not fileid:
            return {'httpcode':0, 'code':self.VIDEO_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid, 'del')
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.post(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
        else:
            return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}


    def generate_res_url(self, userid='0', fileid='', oper=''):
        app_info = conf.get_app_info('video')
        if fileid:
            if oper:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid) + '/' + oper
            else:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid)
        else:
            return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid)

    """分片上传视频文件
	建议较大视频（20M以上）采用分片上传，参数和返回值同upload函数
	"""
    def upload_slice(self, filepath, userid='0',title='',desc='',magic_context=''):
        rsp = self.upload_prepare(filepath,userid,title,desc,magic_context)
        if rsp['httpcode'] != 200 or rsp['code'] != 0:  #上传错误
            if rsp.has_key('data'):
                if rsp['data'].has_key('url'):  #秒传命中
                    return rsp
        offset = 0
        slice_size = 0
        session = ''
        data = rsp['data']
        if data.has_key('slice_size'):
           slice_size = int(data['slice_size'])
        if data.has_key('offset'):
           offset = int(data['offset'])
        if data.has_key('session'):
           session = data['session']
        size = os.path.getsize(filepath)
        fp = open(filepath, 'rb')
        while size > offset:
            data = fp.read(slice_size)
            ret = self.upload_data(userid,data,session,offset)
            if ret['httpcode'] != 200 or ret['code'] != 0:
                return  ret
            if ret.has_key('data'):
                if ret['data'].has_key('url'):
                    return  ret
            offset += slice_size
        return  ret

    #分片上传,控制包/断点续传
    def upload_prepare(self,filepath,userid='0',title='',desc='',magic_context='', session = ''):
        filepath = os.path.abspath(filepath);
        if os.path.exists(filepath):
            url = self.generate_res_url(userid)
            expired = int(time.time()) + self.EXPIRED_SECONDS
            auth = Auth(self._secret_id, self._secret_key)
            sign = auth.app_sign(url, expired)
            size = os.path.getsize(filepath)
            sha1 = hashlib.sha1();
            fp = open(filepath, 'rb')
            sha1.update(fp.read())

            headers = {
                'Authorization':sign,
                'User-Agent':conf.get_ua(),
            }
			
            files = {'op': ('upload_slice'),'Sha':sha1.hexdigest(),'filesize': str(size),'Title':title,'Desc':desc,'MagicContext':magic_context,'session':session}
            r = {}
            try:
                r = requests.post(url, headers=headers,files=files)
                ret = r.json()

            except Exception as e:
                if r:
                    return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
                else:
                    return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
			
            if 'code' in ret:
                if 0 == ret['code']:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':ret['data'],
                    }
                else:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{}
                    }
            else:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

        else:
            return {'httpcode':0, 'code':self.VIDEO_FILE_NOT_EXISTS, 'message':'file not exists', 'data':{}}
			
    #上传二进制流，用于分片上传
    def upload_data(self,userid,data,session,offset):

            url = self.generate_res_url(userid)
            expired = int(time.time()) + self.EXPIRED_SECONDS
            auth = Auth(self._secret_id, self._secret_key)
            sign = auth.app_sign(url, expired)
			
            sha1 = hashlib.sha1();
            sha1.update(data)

            headers = {
                'Authorization':sign,
                'User-Agent':conf.get_ua(),
            }

            files = {'op': ('upload_slice'),'filecontent': data,'session':session,'offset':str(offset)}
            r = {}
            try:
                r = requests.post(url, headers=headers,files=files)
                ret = r.json()

            except Exception as e:
                if r:
                    return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
                else:
                    return {'httpcode':0, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(e), 'data':{}}
			
            if 'code' in ret:
                if 0 == ret['code']:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':ret['data'],
                    }
                else:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{}
                    }
            else:
                return {'httpcode':r.status_code, 'code':self.VIDEO_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}