from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Post
from django.http import HttpResponse
from .Forms import PostCreateForm

User = get_user_model()


def post_list(request):
    post = Post.objects.all().order_by('-created_date')
    context = {
        'title': 'PRIMARY NEWS',
        'post': post,
    }
    return render(request, 'blog/post_list.html', context=context)


def post_detail(request, pk):
    context = {
        'post': Post.objects.get(pk=pk),
    }
    return render(request, 'blog/post_detail.html', context)


def post_create(request):
    if request.method == 'GET':
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_create.html', context)
    elif request.method == 'POST':
        form = PostCreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            user = User.objects.first()
            post = Post.objects.create(
                title=title,
                text=text,
                author=user
            )
            return redirect('post_detail', pk=post.pk)

        else:
            context = {
                'form': form,
            }
            return render(request, 'blog/post_create.html', context)


def post_modify(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        data = request.POST

        title = data['title']
        text = data['text']
        post.title = title
        post.text = text
        post.save()
        return redirect('post_detail', pk=post.pk)
    elif request.method == 'GET':
        context = {
            'post': post
        }
        return render(request, 'blog/post_modify.html', context)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    elif request.method == 'GET':
        return render(request, 'blog/post_modify.html')
