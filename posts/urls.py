from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('like_post/<int:post_id>',like_post,name="like_post"),
    path("add_comment/<int:post_id>",add_comment, name="add_comment"),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('get_more_comments/<int:post_id>/', get_more_comments, name='get_more_comments'),
    path('create_post/', create_post, name='create_post'),
]
