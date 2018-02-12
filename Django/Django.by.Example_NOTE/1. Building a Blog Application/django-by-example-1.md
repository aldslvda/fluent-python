## Dajango By Example Chapter 1. Building a Blog Application
## 搭建一个Blog应用

这一节的内容包括：   
- 安装Django，创建一个project    
- 设计数据模型，生成数据模型的数据库迁移
- 创建一个站点对模型进行管理
- 使用 QuerySet(查询集) and managers(管理器)
- 搭建 视图(views), 模板(templates), 和URL
- 为列表视图添加分页
- 使用Django 的内置类视图 

###  1. 安装Django, 创建一个Django Project
众所周知，Django 是Python的一个Web框架，而且同时兼容Python2.7和Python3,所以我们要先安装Python.
但是由于Django2.0(目前最新版本2.02)开始不兼容Python2.7, 所以直接安装Python3比较靠谱。
Python的安装就不赘述了。
#### 1.1 创建一个独立的Python环境
推荐使用 virtualenv 为你的Django 项目创建独立的Python环境，这样可以对不同的项目单独进行包管理,这样所有的项目都使用系统范围的Python实用的多。    
可以在Shell中运行下面的命令安装virtualenv:   
```shell   
> pip install virtualenv
```
在此之后可以使用下面的命令创建一个独立的Python环境,并激活

```shell   
> virtualenv venv
> source my_env/bin/activate
```
使用deactivate命令可以随时取消venv的激活状态。  
另外,可以使用virtualenvwrapper对virtualenv进行管理,这个工具可以使创建和管理virtualenv变得更加容易。

#### 1.2 使用pip安装Django
进入venv, Shell中运行下面的命令即可:  

```shell
> pip install django
```
#### 1.3 创建一个Django Project
运行下面的命令: 

```shell
> django-admin startproject aldsblog
```

这样我们得到了一个名为aldsblog的project,项目结构如下图所示（暴露了windows >_>：   
![Figure-1-1](https://github.com/aldslvda/blog-images/blob/master/djangobyexample-1.1.png?raw=true)

- manage.py: 用来和项目交互的命令行工具   
- mysite/: 项目目录，包含下面的文件:       
    - \_\_init\_\_.py: 空文件, 让Python 将项目文件夹看作一个module  
    - settings.py: 项目的相关配置(有默认值).  
    - urls.py: 定义url pattarn的文件, 每个url指向一个视图.  
    - wsgi.py: 讲项目作为WSGI应用运行的一系列配置.

自动生成的settings.py文件包含了：使用SQLite的基本设置, Django自动加入到项目中的一系列应用。   
我们需要先为项目创建初始的数据表。

由于我使用的数据库是mysql,所以要对默认的设置做出一些更改：

```python   
# in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aldsblog',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': 'root',
        'PORT': '3306',
        }
}
```

同时需要为python环境安装mysql驱动*mysqlclient*

```shell  
> pip install mysqlclient
```

运行下面的命令进行数据库迁移：

```shell   
> python manage.py migrate
```
控制台会打出log

```    
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK

```
这时候数据库中已经自动生成一系列Django自带模块需要使用的表了。

```sql  
mysql> use aldsblog;
Database changed
mysql> show tables;
+----------------------------+
| Tables_in_aldsblog         |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
10 rows in set (0.00 sec)
```


接下来运行下面的命令将服务器运行起来：

```shell   
> python manage.py runserver
```

我们就可以进入浏览器查看第一个项目了:

![Figure-1-2 Django Project 初始界面](https://github.com/aldslvda/blog-images/blob/master/djangobyexample-1.2.png?raw=true)

需要注意的是, 这个服务器并不适合作为生产环境, 如果在生产环境使用Django作为服务器,需要使用Apache, Gunicorn, 或者 uWSGI将它作为一个Web Server Gateway Interface (WSGI) application运行。

#### 1.4 项目设置

settings.py 的设置可以在[官方文档](https://docs.djangoproject.com/en/2.0/ref/settings/)中查看   

下面这些是值得一看的设置   
- DEBUG 是用来开关调试模式的布尔值，如果是True, Django会在页面上显示详细的错误页面和异常信息。在生产环境应该把它设置为False, 否则可能会泄露项目的敏感信息。  

