from django import forms
from django.forms import ModelForm
from account.models import Post, Comment


class CreateUpdatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', )
        widgets = {"body": forms.Textarea(attrs={"class": "form-control"})}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        widgets = {'text': forms.Textarea(attrs={"class": "form-control"})}

class CommentReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        widgets = {'text': forms.Textarea(attrs={"class": "form-control"})}

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))