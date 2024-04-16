from django import forms
from .models import Product, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('article', 'user',)
