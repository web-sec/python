# python学习笔记
### 安装homebrew
参考网上推荐健的方法，在终端中执行以下命令：
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
### vim修改文件
```
sudo vim 文件名
```
退出：先按esc，后按冒号，然后输入退出方式，wq是保存退出； q!是维持原样退出
### 针对不同版本pyhton安装第三方库

```
sudo python3.6 -m pip install xxx
```
###关于在atom中指定哪个版本的python运行代码
在文件开头（一般是第一行）指定#!pyhton2/3
### idle : 打开python shell
### 安装第三方包可以用easy_install，一次性搞定
### 查看已安装的第三方库：在python环境中输入help('modules')
### python下使用mongodb
- 安装mongodb : 用homebrew安装，一键搞定，之后新建、data/db文件夹，具体看印象笔记
- 安装mongodb可视化工具:robomongo，官网直接下
- 安装第三方包 pymongo
// :整数除法：返回一个最接近但不大于结果的整数

### python基本数据类型：
- integer
- float
- long
- string
- list
- tuple
- dictionary

### 字符串方法
- .upper() 全部大写
- .lower() 全部小写
- .capitalize() 首字母大写，其余小写
- .title() 单词首字母大写，其余小写
- .strip() 删除字符串头尾的空格（或指定的参数）
- .rstrip() 只删除尾部的
- .lstrip() 只删除头部的
- .count() 计算参数字符串在指定字符串中出出现的次数
- .find() 返回参数在指定字符串中第一次出现的位置
- .replace（a,b）将a全部替换为b
- .format()  在字符串中预留{xxx},然后用该方法插入xxx的内容

### 输入
- .input()
- .raw_inpuit() 所有输入都是字符串
- .getpass() 不显示输入信息

###函数
- 传递可变数量参数：1. \**kwargs(多余的参数传递到此字典中) 2.\*args（多余的参数传递到此列表中）

###字典
- .pop(x) 删除键值为x的键值对
- .has_key(x) 字典是否有键值为x的成员
- in语句: x in y y字典是否含有x键

###类
- \__init__(self):设置该类对象的初始值
- \__eq__(self,other):对两个对象进行==判断时定义判断方式
- \__ne__(self,other):对两个对象进行!=判断时定义判断方式
- \__gt__(self,other):对两个对象进行>判断时定义判断方式
- \__lt__(self,other):对两个对象进行<判断时定义判断方式
- \__gte__(self,other):对两个对象进行>=判断时定义判断方式
- \__lte__(self,other):对两个对象进行<=判断时定义判断方式
- \__str__(self,other):对print一个对象时定义方式
- 继承：class sonclass(fatherclass)
- super() 调用父类中的方法

###操作文件
####原生库函数：
- opne(x，y) 打开指定文件x,y为打开方式。有‘r+w’:读写，即打开并添加；‘w’:写，直接覆盖原来的内容；’w+’/'a':如果文件不存在，则创建之
- .close() 关闭文件
- .readline() 逐行读取
- .writeline(x) 将列表x中的值逐行写入
####os库
- os.getcwd() 返回当前目录
- os.listdir(x) 返回x目录下所有文件名（x='.'代表当前目录）
- os.walk()
- os.makedir(x) 创建文件夹x
- os.makedirs(x\\y) 创建嵌套文件夹
- os.stat(x) 路径为x的文件夹的相关数据。st_size:文件大小(字节)；st_mtime:最后访问时间、最后修改时间（UNIX时间）

###json库
- .load(x) 加载JSON对象
- .dump(j,f，indent) 将JSON对象j保存到f文件里,indent是可选参数，能格式化JSON
