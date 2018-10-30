from datetime import datetime

from django.db import models

from tinymce.models import HTMLField

#django 中的模型类必须继承Model类
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名")
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name="昵称")
    password = models.CharField(max_length=50, verbose_name="密码")
    age = models.IntegerField(default=18, verbose_name="年龄")
    gender = models.CharField(default='男', verbose_name="性别", max_length=5)
    email = models.EmailField()
    birthday = models.DateTimeField(auto_now=True)
    # avatar = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.FileField(upload_to="static/upload/")
    objects = models.Manager()

    #用户管理器对象
    # userManager = UserManager()


    def __str__(self):
        return self.username

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    # content = models.TextField()
    content = HTMLField()
    #发表时间
    publishTime = models.DateTimeField(auto_now_add=True)
    #修改时间
    modifyTime = models.DateTimeField(auto_now=True)
    #点击率
    count = models.IntegerField(default=0)

    objects = models.Manager()

    author = models.ForeignKey(Users, on_delete=models.CASCADE)





