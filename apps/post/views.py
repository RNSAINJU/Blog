from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.views.generic import ListView, TemplateView
from .forms import CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

class PostListView(ListView):
    model=Post
    context_object_name = 'posts'
    template_name = 'index.html'

    # def get_queryset(self):
    #     post=Post.objects.all().order_by('id')
    #     queryset={'posts':posts}
    #     return queryset

class PostDetailView(TemplateView):

    def get(self, request, slug):
        form=CommentForm()
        post=get_object_or_404(Post, slug=slug )
        comment=Comment.objects.filter(post__slug=slug)
        queryset={'post':post,'comments':comment,'form':form}
        return render(request,'postdetails.html',queryset)


    def post(self, request,slug):
        if request.user.is_authenticated:
            form=CommentForm(request.POST or None)
            post=get_object_or_404(Post, slug=slug)
            if form.is_valid():
                Comment.objects.create(
                    message=form.cleaned_data.get('message'),
                    post=post,
                    created_by=self.request.user
                )
        else:
            print("Need to login")
        return redirect('post_detail' ,slug=slug)