from django.core.cache import cache

from . import models


# 全部用户信息展示
def getAllUserInfo(ischange=False):
    # print("从缓存中取数据……")
    UserInfo = cache.get("allUserInfo")
    if UserInfo is None or ischange:
        # print("未能从缓存中找到数据，开始从数据库中取……")
        UserInfo = models.Users.objects.all()
        # print("数据库中获取数据成功，将数据保存到缓存中……")
        cache.set("allUserInfo", UserInfo)
    return UserInfo


# 个人信息展示
# def getUserInfo(u_id,ischange=False):
#     # print("从缓存中取数据……")
#     UserInfo = cache.get("UserInfo")
#     if UserInfo is None or ischange:
#         # print("未能从缓存中找到数据，开始从数据库中取……")
#         UserInfo = models.Users.objects.get(pk=u_id)
#         # print("数据库中获取数据成功，将数据保存到缓存中……")
#         cache.set("UserInfo", UserInfo)
#     return UserInfo



# 修改个人信息
# def update_UserInfo(user_id,ischange=False):
#     print("从缓存中取数据……")
#     UserInfo = cache.get("update_UserInfo")
#     if UserInfo is None or ischange:
#         print("未能从缓存中找到数据，开始从数据库中取……")
#         UserInfo = models.Users.objects.get(pk=user_id)
#         print("数据库中获取数据成功，将数据保存到缓存中……")
#         cache.set("update_UserInfo", UserInfo)
#     return UserInfo


# 查看所有文章
def getAllArticle(ischange=False):
    # print("从缓存中取数据……")
    ats = cache.get("allArticles")
    if ats is None or ischange:
        # print("未能从缓存中找到数据，开始从数据库中取……")
        ats = models.Article.objects.all()
        # print("数据库中获取数据成功，将数据保存到缓存中……")
        cache.set("allArticles", ats)
    return ats


# 查看个人发表的文章
def getSelfArticle(author, ischange=False):
    # print("从缓存中取数据……")
    ats = cache.get("selfArticles")
    if ats is None or ischange:
        # print("未能从缓存中找到数据，开始从数据库中取……")
        ats = models.Article.objects.filter(author=author)
        # print("数据库中获取数据成功，将数据保存到缓存中……")
        cache.set("selfArticles", ats)
    return ats


# 文章展示
# def detailArticle(a_id, ischange=False):
#     # print("从缓存中取数据……")
#     ats = cache.get("detailArticles")
#     if ats is None or ischange:
#         # print("未能从缓存中找到数据，开始从数据库中取……")
#         ats = models.Article.objects.get(pk=a_id)
#         # print("数据库中获取数据成功，将数据保存到缓存中……")
#         cache.set("detailArticles", ats)
#     return ats
