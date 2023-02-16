from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ["user", "body", "slug"]
    list_display = ["user", "body"]
    search_fields = ["slug", "body"]
    list_filter = ["created_at"]
    raw_id_fields = ['user']
    prepopulated_fields = {'slug': ('body',)}

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    fields = ["following", "followers"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "text"]

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

admin.site.register(Communication)
admin.site.register(Direct)

