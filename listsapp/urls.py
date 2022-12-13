from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create_list", views.create_list, name="create_list"),
    path("create_list_item/<int:id>", views.create_list_item, name="create_list_item"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("category", views.category, name="category"),
    path("category_individual/<str:title>", views.category_individual, name="category_individual"),    
    path("delete_list/<int:id>", views.delete_list, name="delete_list"),
    path("follow_list/<int:id>", views.follow_list, name="follow_list"),
    path("follow_view", views.follow_view, name="follow_view"),
    path("edit_list/<int:id>", views.edit_list, name="edit_list"),
    path("delete_list_item/<int:id>", views.delete_list_item, name="delete_list_item"),
    path("complete_list_item/<int:id>", views.complete_list_item, name="complete_list_item"),
    path("check_complete/<int:id>", views.check_complete, name="check_complete"),
    path("get_follow/<int:id>", views.get_follow, name="get_follow"),
]