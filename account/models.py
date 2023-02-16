from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, verbose_name="کاربر")
    body = models.TextField(verbose_name="محتوای پست")
    slug = models.SlugField(verbose_name="اسلاگ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def get_absolute_url(self):
        return reverse("home:detail", args=(self.pk, self.slug))

    def __str__(self):
        return self.body

    def get_like_post(self):
        return self.plike.count()


class Relation(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings", verbose_name="فالووینگ")
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name="فالوورز")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.following} followed, {self.followers}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomment", verbose_name="کاربر")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomment", verbose_name="پست")
    text = models.TextField(verbose_name="متن کامنت")
    is_reply = models.BooleanField(default=False, verbose_name="کامنت ریپلای")
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="child_comment",
                              verbose_name="کامنت ریپلای")
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="plike", verbose_name="پست")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ulike", verbose_name="کاربر")


class Profile(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    bio = models.TextField(null=True, blank=True, verbose_name="بیوگرافی")
    age = models.PositiveSmallIntegerField(default=0, verbose_name="سن")

class Communication(models.Model):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request', None)
        super().__init__(*args, **kwargs)

    users = models.ManyToManyField(User, related_name="communications", verbose_name="کاربران")
    name = models.CharField(max_length=50, verbose_name="نام")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_communications_user_private(self):
        user = self.request
        count_users = self.users.count()
        if count_users == 2:
            pv = self.users.all()
            print(pv)
            print(self.request)
            return pv
        elif count_users == 1:
            return "Saved Messages"
        else:
            return self.name

    def __str__(self):
        if self.users.count() == 2:
            return f"{self.users.all()[0]} in communicated with {self.users.all()[1]}"
        else:
            return self.name


class Direct(models.Model):
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE,
                                      related_name="messages",
                                      verbose_name="ارتباط")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sdirect", verbose_name="ارسال کننده")
    view = models.BooleanField(default=False, verbose_name="پیام دیده شده؟")
    body = models.TextField(blank=True, null=True, verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sender {self.body},"

    class Meta:
        ordering = ("created_at",)

    def did_not_view_messages(self, user):
        return self.objects.filter(receiver=user, view=False).count()

    def get_last_text_message(self):
        return self.body
