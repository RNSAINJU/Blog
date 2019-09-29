from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, PostView
from django.views.generic import View,ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm, PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.urls import reverse,reverse_lazy

def get_category_count():
    queryset=Post.objects.values('categories__name').annotate(Count('categories'))
    return queryset

def search(request):
    queryset=Post.objects.all()
    query= request.GET.get('q')
    if query:
        queryset=queryset.filter(
            Q(title__icontains=query)
        # |Q(categories__icontains=query)
        )
        # .distinct()
    context={
        'queryset':queryset
    }
    return render(request,'searchresults.html',context)

class IndexView(View):
    model=Post
    template_name = 'index.html'

    def get(self,request):
        category_count=get_category_count()
        featured=Post.objects.filter(featured=True)
        latest=Post.objects.order_by('-created_at')[0:3]
        queryset={
            'featured':featured,
            'latest':latest,
            'category_count':category_count
        }
        return render(request,self.template_name,queryset)



class PostsListView(ListView):
    model=Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by=1

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        latest = Post.objects.order_by('-created_at')[:3]
        context=super().get_context_data(**kwargs)
        context['latest'] = latest
        context['category_count'] = category_count
        return context


# class PostDetailView(DetailView):
#     model = Post
#     template_name = "postdetails.html"
#     context_object_name = 'post'
#     form= CommentForm()
#
#     def get_object(self):
#         obj=super().get_object()
#         if self.request.user.is_authenticated:
#             PostView.objects.get_or_create(
#                 user=self.request.user,
#                 post=obj
#             )
#         return obj
#
#     def get_context_data(self, **kwargs):
#         category_count=get_category_count()
#         latest=Post.objects.order_by('-created_at')[:3]
#         context=super().get_context_data(**kwargs)
#         context['latest']=latest
#         context['category_count']=category_count
#         context['form']=self.form
#         return context
#
#
#
#     def post(self, request, *args, **kwargs):
#         form=CommentForm(request.POST or None)
#         if form.is_valid():
#             post=self.get_object()
#             form.instance.created_by=request.user
#             form.instance.post=post
#             form.save()
#             return redirect(reverse("post_detail",kwargs={
#                 'slug':post.slug
#             }))
#         return HttpResponse("assa")

def post_detail(request, slug):
    category_count = get_category_count()
    latest =Post.objects.order_by('-created_at')[:3]
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': post.slug
            }))
    context = {
        'post': post,
        'latest': latest,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'postdetails.html', context)

class PostCreateView(CreateView):
    model=Post
    template_name='post_create.html'
    form_class=PostForm

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Create'
        return context

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        form.save()
        return redirect(reverse("post_detail",kwargs={
            'slug':form.instance.slug
        }))

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Update'
        return context

    def form_valid(self, form):
        post=form.save(commit=False)
        post.save()
        return redirect(reverse("post_detail", kwargs={
            'slug': form.instance.slug
        }))



class PostDeleteView(DeleteView):
    model=Post
    success_url='/blog'
    template_name='post_confirm_delete.html'
