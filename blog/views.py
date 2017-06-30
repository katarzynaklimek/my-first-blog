from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.http import HttpResponse

supported_langs = ['pl', 'en']

def post_list(request):
    lang = detect_language(request)
    posts = Post.objects.filter(published_date__lte=timezone.now(), language=lang).order_by('published_date')
    response = render(request, 'blog/post_list.html', {'posts': posts, 'lang': lang})
    response.set_cookie('lang', lang)

    return response

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    lang = detect_language(request)
    return render(request, 'blog/post_detail.html', {'post': post, 'lang': lang})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def detect_language(request):
    lang = request.GET.get('setlang')

    if lang in supported_langs:
        return lang

    lang = request.COOKIES.get('lang')

    if lang in supported_langs:
      return lang

    return 'pl'

def mylang(request):
    return HttpResponse("request.LANGUAGE_CODE = %s\n" % request.LANGUAGE_CODE)
