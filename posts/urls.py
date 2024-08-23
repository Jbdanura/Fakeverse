from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('like_post/<int:post_id>',like_post,name="like_post"),
    path("add_comment/<int:post_id>",add_comment, name="add_comment"),
    path('create_post/', create_post, name='create_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('load_more_comments/<int:post_id>/', load_more_comments, name='load_more_comments'),
    path('news_all/', all_news, name='all_news'),
    path('news_<str:category>/', category_news, name='category_news'),
]
