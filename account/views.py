from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Post, Relation, Communication, Direct
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse
# Create your views here.

class RegisterView(View):
    form_class = RegisterForm
    template_name = "account/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, req):
       form = self.form_class()
       return render(req, self.template_name, {"form": form})

    def post(self, req):
        form = self.form_class(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd.get("username"), email=cd.get("email"), password=cd.get("password"))
            messages.success(req, "You Registered in our website...", extra_tags="success")
            return redirect("home:index")
        return render(req, self.template_name, {"form": form})


class LoginView(View):
    form_class = LoginForm
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            auth = authenticate(request, username=cd["username"], password=cd["password"])
            if auth is not None:
                login(request, user=auth)
                messages.success(request, "You were Login the site...Welocome", extra_tags="success")
                return redirect("home:index")
            messages.error(request, "Your Password or Username is wrong", extra_tags="danger")

        return render(request, self.template_name, {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You Were Logout.....", "secondary")
        return redirect("home:index")

class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        followed = Relation.objects.filter(followers=user, following=request.user).exists()
        posts = Post.objects.filter(user=user)
        return render(request, "account/profile.html", {"user": user, "posts": posts, "followed": followed})

class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/pasword_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")

class UserPasswordResetConfirmDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_confirm_done.html"

class UserFollowView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.current_user = User.objects.get(pk=kwargs.get("userid"))
        self.followed_users = Relation.objects.filter(following=request.user, followers=self.current_user).exists()
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.current_user:
            messages.error(request, "you cant follow yourself ...:)", extra_tags="danger")
            return redirect("account:profile", request.user.id)

        if self.followed_users:
            messages.warning(request, "you followed him...", extra_tags="warning")
            return redirect("account:profile", self.current_user.id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, userid):
        Relation.objects.create(followers=self.current_user, following=request.user)
        return redirect("account:profile", userid)
    
    
class UserUnFollowView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.current_user = User.objects.get(pk=kwargs.get("userid"))
        self.rel = Relation.objects.filter(followers=self.current_user, following=request.user)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.current_user == request.user:
            messages.warning(request, "you can't unfollow yourself ...:)", extra_tags="warning")
            return redirect("account:profile", self.current_user.id)
        if not self.rel.exists():
            messages.warning(request, "you didn't followed him...", extra_tags="warning")
            return redirect("account:profile", self.current_user.id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, userid):
        self.rel.delete()
        return redirect("account:profile", self.current_user.id)

class EditProfileView(LoginRequiredMixin, View):
    form_class = ProfileForm
    def get(self,request,*args,**kwargs):
        return render(request,
                      "account/edit_profile.html",
                      {"form": self.form_class(instance=request.user.profile, initial={"email": request.user.email})})
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email=form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "Your Profile edited...")
            return redirect("account:profile", request.user.id)



# class DirectList(LoginRequiredMixin, View):
#
#     def get(self, request):
#         communications = Communication.objects.filter(users=request.user)
#         communications.
#         return render(request, "account/main_direct.html", {"communications": communications})
