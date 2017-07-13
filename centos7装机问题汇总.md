###问题汇总
1. 装pip
先扩展yum源
```
sudo yum -y install epel-release
```
可能遇到yum被锁，解决办法:
```
sudo rm -f /var/run/yum.pid
```
然后装pip
```
sudo yum -y install python-pip
```
可能要跟新pip
```
sudo pip install --upgrade pip
```
