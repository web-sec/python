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
