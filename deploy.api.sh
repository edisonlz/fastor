#!/bin/bash
#CentOS 部署API脚本

if [ ! -d "/data/downloads" ];then
 mkdir /data/downloads
fi
echo '[start install g++!]'
yum install gcc-c++.x86_64
yum install gcc
yum install gcc-c++
yum install openssl-devel
yum install readline-devel
yum install mysql-devel

echo '[start install nginx]'
yum install nginx



echo '[start install python!]'
cd /data/downloads/
wget http://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz
tar zxf Python-2.7.2.tgz
cd Python-2.7.2
./configure --prefix=/data/python2.7
make
make install
export PATH=/data/python2.7/bin:$PATH
echo "export PATH=/data/python2.7/bin:\$PATH" > /etc/profile.d/python.sh

cd /data/downloads/
wget  --no-check-certificate https://codeload.github.com/farcepest/MySQLdb1/zip/utf8mb4
unzip utf8mb4
cd MySQLdb1-utf8mb4/
/data/python2.7/bin/python  setup.py install




echo "make logs dir"
mkdir -p /data/logs/nginx/access
mkdir -p /data/logs/nginx/error
mkdir -p /data/logs/nginx/statis
mkdir -p /data/logs/tornado
mkdir -p /data/run

ln -s /data/python/fastor/api/conf/nginx/lua /data/nginx/conf/lua
ln -s /data/python/fastor/api/conf/nginx/nginx.conf /data/nginx/conf/nginx.conf
ln -s /data/python/fastor/api/conf/nginx/api.cms.x-transforms.com /data/nginx/conf/api.cms.x-transforms.com


echo "start nginx"
ldconfig
/data/nginx/sbin/nginx -c /data/nginx/conf/nginx.conf


echo '[start install crontabs!]'
yum install crontabs

#################################################
echo '[start install log rotate!]'

#Edit crontab file
#1.部署日志切割，每天0点生成前一天的日志文件
#2.删除大于7天的日志
num=$( cat /var/spool/cron/root|grep -c logrotate-nginx ) 
if [ $num = 0 ];then 
   echo "OK-O-O-O write hosts"
   read i
   echo '0 0 * * * /data/python/fastor/api/bin/logrotate-nginx.sh > /dev/null 2>&1'>>/var/spool/cron/root
   echo '5 0 * * * /data/python/fastor/api/bin/logrotate.sh > /dev/null 2>&1'>>/var/spool/cron/root
   echo '#Delete old more than 7 days log files'>>/var/spool/cron/root
   echo '22 2 * * * find /data/logs/ -mtime +7 -type f -name "*log*" -exec rm -rf {} \;'>>/var/spool/cron/root
fi


#register service
chmod +x /data/python/fastor/api/main.py
chmod +x /data/python/fastor/api/bin/*

cp /data/python/fastor/api/bin/init.d/tornado /etc/init.d/
cp /data/python/fastor/api/bin/init.d/nginx /etc/init.d/

chkconfig --add nginx
chkconfig nginx on
chkconfig --add tornado
chkconfig tornado on




