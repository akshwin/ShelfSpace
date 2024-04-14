from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Upvote

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        post = BlogPost.objects.create(title=title, content=content, author=author)
        return redirect('ShelfSpaceBlogs:post_list')
    return render(request, 'ShelfSpaceBlogs/create_post.html')

def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'ShelfSpaceBlogs/post_blog.html', {'posts': posts})

@login_required
def upvote_post(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    if request.user != post.author and request.user not in post.upvoted_users.all():
        upvote = Upvote.objects.create(user=request.user, post=post)
        post.upvoted_users.add(request.user)
        post.save()
    return redirect('blog:post_list')