#!/bin/bash

#Centos 部署脚本
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


echo "[install pip]"
yum install pip

echo "[install supervisord]"
pip install supervisord


echo "make logs dir"
mkdir -p /data/logs/nginx/access
mkdir -p /data/logs/nginx/error
mkdir -p /data/logs/nginx/statis
mkdir -p /data/logs/tornado
mkdir -p /data/run


#启动memcached
echo "[setup memcached ]"
yum install memcached
/usr/bin/memcached -d -U 11211 -p 11211 -u nobody -m 200 -c 10000 -P /var/run/memcached/memcached.11211.pid

echo "[setup redis]"
yum install redis
service redis start


echo "start app"
cd /data/python/fastor/app
chmod u+x app.sh
./app.sh restart


echo "start nginx"
rm -rf /data/nginx/conf/nginx.conf
ln -s /data/python/fastor/app/conf/nginx.conf /data/nginx/conf/nginx.conf
ln -s /data/python/fastor/app/conf/api.fastor.com /data/nginx/conf/api.fastor.com

ldconfig
/data/nginx/sbin/nginx -c /data/nginx/conf/nginx.conf




