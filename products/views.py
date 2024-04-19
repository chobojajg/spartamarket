from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Comment
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods


def index(request):
    if request.user.is_authenticated:
        articles = Product.objects.all().order_by('-created_at')
        context = {
            'articles': articles,
        }
        return render(request, 'products/index.html', context)
    else:
        return redirect('accounts:login')


@login_required
def article_detail(request, pk):
    article = get_object_or_404(Product, pk=pk)  # Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comments.all().order_by('-pk')
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'products/article_detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('products:article_detail', article.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'products/create.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    article = get_object_or_404(Product, pk=pk)
    if article.author == request.user:
        if request.method == "POST":  # update
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                article = form.save()
                return redirect('products:article_detail', article.pk)
        else:  # 수정
            form = ArticleForm(instance=article)
    else:
        return redirect('products:index')

    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'products/update.html', context)


@login_required
@require_POST
def delete(request, pk):
    article = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        if article.author == request.user:
            article = get_object_or_404(Product, pk=pk)
            article.delete()
    return redirect('products:index')


@login_required
@require_POST
def comment_create(request, pk):
    article = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect('products:article_detail', article.pk)


@login_required
@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect('products:article_detail', pk)


@login_required
@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Product, pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect('accounts:login')
