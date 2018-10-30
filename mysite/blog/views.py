from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import  redirect
from django.http import HttpResponse
from django.http import JsonResponse
# from mysite import settings
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# 分页插件在core包中
from django.core.paginator import Paginator

from io import BytesIO
import math

from . import models
from . import utils
from . import cacheUtils


def index(request):
    return render(request, "blog/blog.html", {})


# ajax查验用户名
# @csrf_exempt表示忽略跨域请求伪造
@csrf_exempt
@require_POST
def checkusername(request):
    username = request.POST["username"]
    try:
        models.Users.objects.get(username=username)
        return JsonResponse({"msg":"用户名已存在", "success":False})
    except:
        return JsonResponse({"msg": "可以注册", "success": True})


# ajax查验昵称
@csrf_exempt
@require_POST
def checknickname(request):
    nickname = request.POST["nickname"]
    try:
        models.Users.objects.get(nickname=nickname)
        return JsonResponse({"msg":"昵称已存在", "success":False})
    except:
        return JsonResponse({"msg": "可以注册", "success": True})


# 用户登录
def login(request):
    if request.method == "GET":
        return render(request, "blog/login.html", {})
    elif request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        mycode = request.POST.get("code", None)
        # 验证码的验证
        session_code = request.session["code"]

        # 首先判断验证码是否正确
        if mycode == None or session_code.upper() != mycode.strip().upper():
            # 清除验证码
            del request.session["code"]
            return render(request, "blog/login.html", {"msg": "验证码错误，请正确填入验证码"})

        # 对密码加密
        pwd = utils.hamcByMD5(password, settings.MD5_SALT)
        try:
            user = models.Users.objects.get(username=username, password=pwd)
            # 登录成功， 保存用户的登录状态
            request.session["loginUser"] = user
            return render(request, "index.html", {})
        except:
            return render(request, "blog/login.html", {"msg": "用户名或者密码错误，请重新输入！！"})


# 注册
def register(request):
    if request.method == "GET":
        return render(request, "blog/register.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        username = request.POST["username"]
        nickname = request.POST["nickname"]
        password = request.POST["password"]
        confirmpwd = request.POST["confirmpwd"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        age = request.POST["age"]
        mycode = request.POST.get("code", None)

        # 第一种上传文件的方法
        # path = "static/upload/" + avatar.name
        # with open(path, "wb") as file:
        #     for f in avatar.chunks():
        #         file.write(f)


        # 验证码的验证
        session_code = request.session["code"]
        # 首先判断验证码是否正确
        if mycode == None or session_code.upper() != mycode.strip().upper():
            # 清除验证码
            del request.session["code"]
            return render(request, "blog/register.html", {"msg": "验证码错误，请正确填入验证码"})

        # 数据校验
        if len(username) < 6:
            return render(request, "blog/register.html", {"msg": "用户名不能小于6位"})
        if len(nickname) == 0:
            return render(request, "blog/register.html", {"msg": "昵称不能为空"})
        if len(password) < 6:
            return render(request, "blog/register.html", {"msg": "密码不能小于6位"})
        if password != confirmpwd:
            return render(request, "blog/register.html", {"msg": "两次密码不一致！！"})
        if len(email) == 0:
            return render(request, "blog/register.html", {"msg": "邮箱不能为空"})

        # 判断用户名是否存在
        try:
            models.Users.objects.get(username=username)
            return render(request, "blog/register.html", {"msg": "该用户已存在，请重新输入！！"})
        except:
            try:
                # 数据验证通过
                # 加密密码
                pwd = utils.hamcByMD5(password, settings.MD5_SALT)
                user = models.Users(username=username, nickname=nickname, password=pwd, gender=gender, email=email,age=age)
                try:
                    avatar = request.FILES["avatar"]
                    user.avatar = avatar
                except:
                    user.avatar = "static/img/Img2.png"
                user.save()
                try:
                    del request.session["loginUser"]
                except:
                    pass
                return render(request, "blog/login.html", {"msg": "注册成功，请登录"})
            except:
                return render(request, "blog/register.html", {"msg": "注册失败，请重新注册"})


# 登出
def logout(request):
    """
    退出登录，清除session中的数据
    :param request:
    :return:
    """
    try:
        del request.session["loginUser"]
    except:
        pass
    return render(request, "blog/login.html", {"msg": "成功退出账号，请登录"})


# 个人信息展示
def show(request, u_id):
    user =models.Users.objects.get(pk=u_id)
    return render(request, "blog/show.html", {"user": user})


# 全部用户信息展示
def list_user(request):
    users =cacheUtils.getAllUserInfo()
    return render(request, "blog/list.html", {"users": users})


# 删除个人信息
def delete(reqeust, user_id):
    user = models.Users.objects.get(pk=user_id)
    user.delete()
    # return HttpResponseRedirect("/blog/list_user/")
    # return HttpResponseRedirect(reverse("blog:list_user"))
    return redirect(reverse("blog:list_user"))


# 修改个人信息
def update(request, user_id):
    if request.method == "GET":
        user = models.Users.objects.get(pk=user_id)
        return render(request, "blog/update.html", {"user": user})
    elif request.method == "POST":
        nickname = request.POST["nickname"]
        age = request.POST["age"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        avatar1 = request.session["loginUser"].avatar
        user = request.session["loginUser"]
        # 头像修改
        try:
            avatar = request.FILES["avatar"]
            user.avatar = avatar
        except:
            user.avatar = avatar1
        user.nickname = nickname
        user.age = age
        user.email = email
        user.gender = gender
        user.save()
        request.session["loginUser"] = user
        # user = models.Users(nickname=nickname, gender=gender, email=email, age=age, avatar=avatar)
        # user.save()
        if user.username=="administrator":
            return redirect(reverse("blog:list_user"))
        else:
            return render(request, "blog/show.html", {"user": user})


# 修改密码
def changepwd(request):
    if request.method == "GET":
        return render(request, "blog/changepwd.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        oldpwd = request.POST["oldpwd"]
        newpwd = request.POST["newpwd"]
        confirmpwd = request.POST["confirmpwd"]
        user = request.session["loginUser"]
        mycode = request.POST.get("code", None)
        # 旧密码加密
        old_hashpwd = utils.hamcByMD5(oldpwd, settings.MD5_SALT)

        # 验证码的验证
        session_code = request.session["code"]
        # 首先判断验证码是否正确
        if mycode == None or session_code.upper() != mycode.strip().upper():
            # 清除验证码
            del request.session["code"]
            return render(request, "blog/register.html", {"msg": "验证码错误，请正确填入验证码"})

        # 数据校验
        if old_hashpwd !=user.password:
            return render(request, "blog/changepwd.html", {"msg": "旧密码输入错误"})
        if len(newpwd) < 6 or len(confirmpwd) < 6:
            return render(request, "blog/changepwd.html", {"msg": "密码不能小于6位"})
        if newpwd != confirmpwd:
            return render(request, "blog/changepwd.html", {"msg": "两次输入密码不一致！！"})

        # try:
        #     models.Users.objects.get(username=username)
        #     return render(request, "blog/register.html", {"msg": "该用户已存在，请重新输入！！"})
        # except:
        try:
            # 数据验证通过
            # 加密密码
            pwd = utils.hamcByMD5(newpwd, settings.MD5_SALT)
            user.password = pwd
            user.save()
            try:
                del request.session["loginUser"]
            except:
                pass
            return render(request, "blog/login.html", {"msg": "修改成功，请重新登录"})
        except:
            return render(request, "blog/changepwd.html", {"msg": "修改失败，请重新修改"})


# 写文章
def write_article(request):
    if request.method == "GET":
        return render(request, "blog/write_article.html", {})
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST['content']
        # 验证非空 合法
        if len(title) == 0  :
            return render(request, "blog/write_article.html", {"msg": "标题不能为空"})
        if len(title)>200:
            return render(request, "blog/write_article.html", {"msg": "标题不能太长"})
        if len(content) == 0:
            return render(request, "blog/write_article.html", {"msg": "内容不能为空"})

        author = request.session["loginUser"]
        article = models.Article(title=title, content=content, author=author)
        article.save()
        return redirect(reverse("blog:detail_article", kwargs={"a_id": article.id}))


# 文章展示
def detail_article(request, a_id):
    article =models.Article.objects.get(pk=a_id)
    article.count += 1
    article.save()
    return render(request, "blog/detail.html", {"article": article})


# 删除文章
def delete_article(request, a_id):
    article = models.Article.objects.get(id=a_id)
    article.delete()
    return redirect(reverse("blog:all_arts"))


# 修改文章
def update_article(request, a_id):
    if request.method == "GET":
        article = models.Article.objects.get(id=a_id)
        return render(request, "blog/update_article.html", {"article": article})
    elif request.method == "POST":
        article = models.Article.objects.get(pk=a_id)
        title = request.POST.get("title")
        content = request.POST['content']
        # 验证非空 合法
        if len(title) == 0:
            return render(request, "blog/update_article.html", {"msg": "标题不能为空"})
        if len(title) > 200:
            return render(request, "blog/update_article.html", {"msg": "标题不能太长"})
        if len(content) == 0:
            return render(request, "blog/update_article.html", {"msg": "内容不能为空"})
        article.title = title
        article.content = content
        article.save()
        # return render(request, "blog/update_article.html", {"article": article})
        return redirect(reverse("blog:detail_article", kwargs={"a_id":a_id}))


# 显示个人文章
def self_article(request):
    author = request.session["loginUser"]
    articles =cacheUtils.getSelfArticle(author).order_by("-publishTime")
    # 分页
    pageNow = int(request.GET.get("pageNow",1))
    pageSize = settings.PAGE_SIZE
    paginator = Paginator(articles,pageSize)
    page = paginator.page(pageNow)

    return render(request, "blog/self_art.html", {"page":page})


# 显示全部文章
def all_arts(request):
    ats = cacheUtils.getAllArticle().order_by("-publishTime")

    # # 分页
    # # 当前页
    # pageNow = int(request.GET.get("pageNow", 1))
    # # 每页显示条数
    # pageSize = int(request.GET.get("pageSize", settings.PAGE_SIZE))
    # # 总记录数
    # allCount = len(ats)
    # # 总页数
    # pageCount = math.ceil(allCount / pageSize)
    # pageCount = range(1,int(pageCount)+1)
    # ats = ats[(pageNow-1)*pageSize:pageNow*pageSize]
    # return render(request, "blog/all_arts.html", {"articles": ats, "pageNow":pageNow, "pageSize":pageSize, "allCount":allCount, "pageCount":pageCount})
    pageNow = int(request.GET.get("pageNow", 1))
    pageSize = settings.PAGE_SIZE
    paginator = Paginator(ats, pageSize)
    page = paginator.page(pageNow)

    return render(request, "blog/all_arts.html", {"page": page})


# 验证码
def code(request):
    img,mycode = utils.create_code()
    request.session["code"] = mycode
    bio = BytesIO()
    img.save(bio,'PNG')
    # print(mycode)
    return HttpResponse(bio.getvalue(), 'image/png')


