from django.urls import path, re_path, include
from .views import *

app_name = "home"

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('post/detail/<int:pk>/<slug:slug>/', DetailPost.as_view(), name="detail"),
    path('post/detail/reply/<int:pk>/<slug:slug>/<int:comment_id>/', CreateReplyCommentView.as_view(), name="comment_reply"),
    path('post/delete/<int:pk>/<slug:slug>/', DeletePostView.as_view(), name="delete"),
    path('post/like/<int:pk>/<slug:slug>/', VoteView.as_view(), name="vote"),
    path('post/unlike/<int:pk>/<slug:slug>/', UnVoteView.as_view(), name="unvote"),
    path('post/update/<int:pk>/', UpdatePostView.as_view(), name="update"),
    path('post/create/', CreatePostView.as_view(), name="create"),
]
