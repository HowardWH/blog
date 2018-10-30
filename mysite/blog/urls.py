from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^index/$", views.index, name="index"),
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^register/$", views.register, name="register"),
    url(r"^(?P<u_id>\d+)/show/$", views.show, name="show"),
    url(r"^list_user/$", views.list_user, name="list_user"),
    url(r"^delete/(?P<user_id>\d+)/$", views.delete, name="delete"),
    url(r"^update/(?P<user_id>\d+)/$", views.update, name="update"),
    url(r"^changepwd/$", views.changepwd, name="changepwd"),
    url(r"^code/$", views.code, name="code"),
    url(r"^write_article/$", views.write_article, name="write_article"),
    url(r"^update_article/(?P<a_id>\d+)/$", views.update_article, name="update_article"),
    url(r"^delete_article/(?P<a_id>\d+)/$", views.delete_article, name="delete_article"),
    url(r"^detail_article/(?P<a_id>\d+)/$", views.detail_article, name="detail_article"),
    url(r"^self_article/$", views.self_article, name="self_article"),
    url(r"^all_arts/$", views.all_arts, name="all_arts"),
    url(r"^checkusername/$", views.checkusername, name="checkusername"),
    url(r"^checknickname/$", views.checknickname, name="checknickname"),

]