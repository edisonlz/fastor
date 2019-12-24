
#!/bin/bash



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

echo '[start install pcre!]'
cd /data/downloads/
wget -O pcre-8.32.tar.gz http://sourceforge.net/projects/pcre/files/pcre/8.32/pcre-8.32.tar.gz/download
tar zxvf pcre-8.32.tar.gz
cd pcre-8.32
./configure
make
make install

cd /lib64/
ln -s libpcre.so.0.0.1 libpcre.so.1
ldconfig

echo '[start install zlib!]'
cd /data/downloads/
wget http://prdownloads.sourceforge.net/libpng/zlib-1.2.7.tar.gz?download
tar zxvf zlib-1.2.7.tar.gz?download
cd  zlib-1.2.7
./configure --prefix=/usr/local
make 
make install




cd /data/downloads/ 
wget http://www.lua.org/ftp/lua-5.1.2.tar.gz
tar zxvf lua-5.1.2.tar.gz
cd lua-5.1.2
make linux
make install

cd /data/downloads/ 
wget http://luajit.org/download/LuaJIT-2.0.0.tar.gz
tar zxvf LuaJIT-2.0.0.tar.gz
cd LuaJIT-2.0.0
make
make install

cd /data/downloads/ 
wget https://codeload.github.com/simpl/ngx_devel_kit/tar.gz/v0.2.17rc2
tar zxvf v0.2.17rc2

cd /data/downloads/ 
wget https://codeload.github.com/openresty/lua-nginx-module/tar.gz/v0.7.8
tar zxvf v0.7.8

export LUAJIT_LIB=/usr/local/lib 
export LUAJIT_INC=/usr/local/include/luajit-2.0

#vim .bash_profile 
#lua问题
#http://blog.sina.com.cn/u/1155571747

num=$( cat /root/.bash_profile|grep -c LUAJIT_LIB ) 
if [ $num = 0 ];then 
   echo "OK-O-O-O write hosts"
   read i
   echo 'export LUAJIT_LIB=/usr/local/lib'>> /root/.bash_profile
   echo 'export LUAJIT_INC=/usr/local/include/luajit-2.0'>> /root/.bash_profile
fi 


echo '[start install nginx-1.0.4!]'
cd /data/downloads/
wget http://nginx.org/download/nginx-1.0.4.tar.gz
tar zxvf nginx-1.0.4.tar.gz
cd nginx-1.0.4
./configure --prefix=/data/nginx --add-module=/data/downloads/ngx_devel_kit-0.2.17rc2 --add-module=/data/downloads/lua-nginx-module-0.7.8   --with-pcre=/data/downloads/pcre-8.32  --with-http_stub_status_module --with-http_ssl_module --with-cc-opt="-Wno-unused-but-set-variable"
make
make install


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

echo "[setup setuptools from ]"
cd /data/downloads/
wget --no-check-certificate  http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74etar zxvf setuptools-0.6c11.tar.gz
tar zxvf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
/data/python2.7/bin/python setup.py install

cd /data/downloads/
wget  --no-check-certificate https://codeload.github.com/farcepest/MySQLdb1/zip/utf8mb4
unzip utf8mb4
cd MySQLdb1-utf8mb4/
/data/python2.7/bin/python  setup.py install

cd /data/downloads/
wget https://pypi.python.org/packages/source/r/rsa/rsa-3.4.tar.gz#md5=9e78250000664a0be51966951d06cc17
tar zxf rsa-3.4.tar.gz
cd rsa-3.4
/data/python2.7/bin/python  setup.py install


echo "[install supervisord]"
cd /data/downloads/
wget https://github.com/Supervisor/supervisor/archive/3.0a10.tar.gz --no-check-certificate
tar zxvf 3.0a10.tar.gz
cd supervisor-3.0a10
/data/python2.7/bin/python setup.py install


echo "make libevent"
cd /data/downloads/
wget https://github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz
tar zxf libevent-2.0.20-stable.tar.gz
cd libevent-2.0.20-stable
./configure 
make 
make install

echo "make libmemcached"
cd /data/downloads/
wget https://launchpadlibrarian.net/91217116/libmemcached-1.0.4.tar.gz
tar zxf libmemcached-1.0.4.tar.gz
cd libmemcached-1.0.4
./configure 
make 
make install

export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
sudo ldconfig
# /etc/ld.so.conf
# add /usr/local/lib/

echo "/usr/local/lib/" >> /etc/ld.so.conf
ldconfig

/etc/ld.so.conf
echo "pylibmc"
cd /data/downloads/
wget https://pypi.python.org/packages/23/f4/3904b7171e61a83eafee0ed3b1b8efe4d3c6ddc05f7ebdff1831cf0e15f1/pylibmc-1.5.1.tar.gz#md5=9077704e34afc8b6c7b0b686ae9579de --no-check-certificate
tar zxf pylibmc-1.5.1.tar.gz
cd pylibmc-1.5.1
/data/python2.7/bin/python setup.py install


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


yum install crontabs

#################################################
#Edit crontab file
num=$( cat /var/spool/cron/root|grep -c logrotate-nginx ) 
if [ $num = 0 ];then 
   echo "OK-O-O-O write hosts"
   read i
   echo '0 0 * * * /data/python/fastor/api/bin/logrotate-nginx.sh > /dev/null 2>&1'>>/var/spool/cron/root
   echo '5 0 * * * /data/python/fastor/api/bin/logrotate.sh > /dev/null 2>&1'>>/var/spool/cron/root
   echo '#Delete old more than 7 days log files'>>/var/spool/cron/root
   echo '22 2 * * * find /data/logs/ -mtime +7 -type f -name "*log*" -exec rm -rf {} \;'>>/var/spool/cron/root
fi

wget https://pypi.python.org/packages/source/r/rsa/rsa-3.4.tar.gz#md5=9e78250000664a0be51966951d06cc17 --no-check-certificate
tar zxf rsa-3.4.tar.gz
cd rsa-3.4
python setup.py install

#register service
chmod +x /data/python/fastor/api/main.py
chmod +x /data/python/fastor/api/bin/*

cp /data/python/fastor/api/bin/init.d/tornado /etc/init.d/
cp /data/python/fastor/api/bin/init.d/nginx /etc/init.d/

chkconfig --add nginx
chkconfig nginx on
chkconfig --add tornado
chkconfig tornado on

#pip切换源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple [packet]

#
pip install scipy
pip install numpy
pip install --upgrade imutils
pip install opencv-python

