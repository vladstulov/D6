from django.forms import ModelForm
from .models import News, Category

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text', 'author', 'category']