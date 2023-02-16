from django.contrib import admin
from django.urls import path, re_path, include
from .views import *

app_name = "account"

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/<int:pk>', UserProfileView.as_view(), name="profile"),
    path('reset/', UserPasswordResetView.as_view(), name="reset_password"),
    path('reset/done/', UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('confirm/complete/', UserPasswordResetConfirmDoneView.as_view(), name="password_reset_complete"),
    path('follow/<int:userid>/', UserFollowView.as_view(), name="follow"),
    path('unfollow/<int:userid>/', UserUnFollowView.as_view(), name="unfollow"),
    path("edit-profile/", EditProfileView.as_view(), name="edit_profile"),
    # path("direct_list/", DirectList.as_view(), name="direct_list"),
]
