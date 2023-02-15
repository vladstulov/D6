from django_filters import FilterSet
from .models import News, Category

class NewsFilter(FilterSet):
   class Meta:
        model = News
        fields = {
            'title': ['icontains'],
            'dateCreation' : ['lt'],
            'text': ['icontains'],
            'author': ['in'],
            'category': ['in'],

        }