from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True)
    def __str__(self):
        return self.name
class News(models.Model):
    title = models.CharField(max_length=50, unique=True)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='news')

    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='news')

    def preview(self):
        preview = f'{self.text[:124]} ...'

        return preview

    def __str__(self):
        return f'{self.title.title()}. Дата публикации: {self.dateCreation.strftime("%d %B, %Y")}. {self.text[:50]}...'
    def get_absolute_url(self):
        return f'/news/{self.id}'

