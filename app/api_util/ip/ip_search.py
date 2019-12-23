#coding=utf-8
import os, sys
import struct, time
from ip2Region import Ip2Region
import logging

def get_file_db():
    CURRENT_ROOT = os.path.realpath(os.path.dirname(__file__))
    file_path = os.path.join(CURRENT_ROOT,"data", 'ip2region.db')
    return file_path


ip_searcher = Ip2Region(get_file_db())

def search_ip(ip):
    global ip_searcher
    
    if not ip_searcher.isip(ip):
        return ""

    data = ip_searcher.btreeSearch(ip)
    return data

def get_ip_info(ip):
    data = search_ip(ip)
    if data:
        city_id = data.get("city_id")
        area = data.get("region","")
        datas = area.split('|')
        province = datas[-3]
        city = datas[-2]
        return city_id, area, province, city
    else:
        return 0,"","",""


def ip_is_ios_check(ip):
    data = search_ip(ip)
    if not data:
        return False
    
    try:
        for area in [166,3399,3400,3401,3402,3403,3403,3404,165,15,20]:
            if area == data.get("city_id",1):
                return True
    except Exception,e:
        logging.error(e)
    
    return False

class IpToRegionSearch(object):

    def __init__(self):
        pass

    @classmethod
    def search(cls,ip):
        data =  search_ip(ip)
        r = {}
        if data:
            datas = data.get("region").split("|")
            #城市Id|国家|区域|省份|城市|ISP
            r = {
                "city_id":data.get("city_id",1),
                "country":datas[0],
                "area":datas[1],
                "province":datas[2],
                "city":datas[3],
                "isp":datas[4],
            }
        return r



if __name__ == "__main__":
    #2351，中国|华南|广西壮族自治区|玉林市|移动
    #城市Id，国家|区域|省份|城市|ISP
    data =  search_ip('117.181.70.53')
    print data
    
  




