from django.shortcuts import render,redirect
from .forms import PostCreateForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.
from .models import Post

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user # estabilished connection b/w user and post
            new_post.save()
            return redirect('feed')
    else:
        form = form = PostCreateForm(data=request.GET)
    
    return render(request,'posts/create.html',{'form':form})


@login_required
def feed(request):
    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        new_comment.post = post #establishing connection b/w post and comment
        new_comment.save()
        return redirect('feed')
    else:
        comment_form = CommentForm()

    posts = Post.objects.all()
    logged_user = request.user

    return render(request,'posts/feed.html',{'posts':posts,'logged_user':logged_user,'comment_form':comment_form})

def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post,id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)

    return redirect('feed')