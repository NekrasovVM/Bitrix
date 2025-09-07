from main import views
from django.urls import path, re_path

urlpatterns = [
    re_path(r'^addition', views.addition),
    re_path(r'^top', views.top),
    path('like/<int:id>', views.like, name="like"),
    path('dislike/<int:id>', views.dislike, name="dislike"),
    # path("postquote/", views.postquote),
    path('', views.index)
]
