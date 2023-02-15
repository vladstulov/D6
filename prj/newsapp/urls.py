from django.urls import path
from .views import NewsList, NewsDetail, NewsSearchList, NewsAddList, NewsEditView, NewsDeleteView, CategoryListView, subscribe, unsubscribe
# импортируемые из файла вьювс внутри этого приложения ньюсап Классы и функции

urlpatterns = [
    path('', NewsList.as_view()),
    path('search', NewsSearchList.as_view()),
    path('add', NewsAddList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name = 'note'),
    path('<int:pk>/edit', NewsEditView.as_view(), name = 'newsEdit'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name = 'newsDelete'),

    path('categories/<int:pk>', CategoryListView.as_view(), name = 'category_list'),

    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    # тк это функция нам не надо писать .эс_вьюв, <адрес, название функции во вьюв, нэйм по которому обращаемся>


    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]
