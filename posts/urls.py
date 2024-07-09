from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('post/',post_view,name="post"),
    path("add_comment/<int:post_id>",add_comment, name="add_comment")
]
