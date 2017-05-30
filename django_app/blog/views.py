from django.shortcuts import render
from .models import Post


def post_list(request):
    post = Post.objects.all().order_by('-created_date')
    context = {
        'title': 'PRIMARY NEWS',
        'post': post,
    }
    return render(request, 'blog/post_list.html', context=context)
