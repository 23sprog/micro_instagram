from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View
from account.models import Post, Comment, Vote
from django.contrib import messages
from django.utils.text import slugify
from .forms import CreateUpdatePostForm, CommentForm, CommentReplyForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.


class HomeView(View):

    def get(self, request):
        form = SearchForm
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = Post.objects.filter(body__contains=request.GET["search"])
        return render(request, "index.html", {"posts": posts, "form": form})

class DetailPost(View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs.get("pk"), slug=kwargs.get("slug"))
        self.form = CommentForm
        self.is_like = Vote.objects.filter(post= self.post_instance, user=request.user).exists()
        return super().setup(request, *args, **kwargs)

    def get(self, request, pk, slug):
        return render(request, "detail_post.html",{"post": self.post_instance,
                    "comments": self.post_instance.pcomment.filter(is_reply=False),
                    "form": self.form,
                    "is_like": self.is_like
                                                   })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            return redirect('home:detail', self.post_instance.pk, self.post_instance.slug)



class DeletePostView(View):

    def get(self, request, pk, slug):
        post = Post.objects.get(pk=pk, slug=slug)
        if post.user == request.user:
            post.delete()
            messages.success(request, "Your Post Successfully Deleted!", extra_tags="success")
        return redirect("home:index")


class UpdatePostView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.intance_post = get_object_or_404(Post, pk=kwargs["pk"])
        self.form_class = CreateUpdatePostForm
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.intance_post.user:
            messages.error(request, "you cant update this post...", extra_tags="danger")
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "update_post.html", {"form": self.form_class(instance=self.intance_post)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.intance_post)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data.get("body")[:30])
            new_post.save()
            return redirect("home:detail", new_post.id, new_post.slug)

class CreatePostView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.form=CreateUpdatePostForm
        return super(CreatePostView, self).setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, "create_post.html", {"form":self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data.get("body")[:30])
            new_post.user = request.user
            new_post.save()
            return redirect("home:detail", new_post.id, new_post.slug)

class CreateReplyCommentView(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs.get("slug"), pk=kwargs.get("pk"))
        self.comment = get_object_or_404(Comment, pk=kwargs.get("comment_id"))
        self.form_class = CommentReplyForm
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "create_reply_comment.html",
                      {"post": self.post_instance,
                        "form": self.form_class,
                        "comments": self.post_instance.pcomment.filter(is_reply=False),
                        "comment_reply": self.comment,
                        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.is_reply = True
            reply_comment.post=self.post_instance
            reply_comment.reply = self.comment
            reply_comment.save()
            return redirect("home:detail", self.post_instance.pk, self.post_instance.slug)

class VoteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get("pk"), slug=kwargs.get("slug"))
        is_like = Vote.objects.filter(post=post, user=request.user)
        if is_like.exists():
            messages.error(request, "You were like this post...", extra_tags="danger")
            return redirect("home:detail", post.id, post.slug)
        else:
            Vote(post=post, user=request.user).save()
            return redirect("home:detail", post.id, post.slug)

class UnVoteView(LoginRequiredMixin, View):
    def get(self, req, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"), slug=kwargs.get("slug"))
        is_like = Vote.objects.filter(post=post, user=req.user)
        if is_like.exists():
            is_like.delete()
            messages.success(req, "You were unlike this post...", extra_tags="danger")
            return redirect("home:detail", post.id, post.slug)
        else:
            messages.error(req, "You weren't like this post...", extra_tags="danger")
            return redirect("home:detail", post.id, post.slug)

