from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from products.models import Product


@login_required
def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    followings = member.following.all()
    followers = member.followers.all()
    articles = Product.objects.all().order_by('-created_at')
    context = {
        "member": member,
        "articles": articles,
        "followings": followings,
        "followers": followers,
    }
    return render(request, "users/profile.html", context)


@login_required
@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("users:profile", username=member.username)
    return redirect("accounts:login")
