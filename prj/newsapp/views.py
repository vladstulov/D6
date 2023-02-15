from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News, Category
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .filters import NewsFilter  # импортируем написанный фильтр
from .forms import NewsForm  # импортируем форму
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Импортуем миксины проверки аутентификации и авторизации

class NewsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = News
    template_name = 'newsapp/news.html'
    context_object_name = 'news'  # имя списка, в котором будут лежать все объекты
    queryset = News.objects.order_by('-dateCreation')
    ordering = ['-dateCreation']
    paginate_by = 4
    permission_required = 'newsapp.view_news'

    def get_context_data(self, **kwargs):
    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['form'] = NewsForm()
        context['newsListLength'] = News.objects.all()
     # на основной странице просмотра новостей добавляем метод для кнопки кнопку Стать автором
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class NewsSearchList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'newsapp/newsSearch.html'  # указываем имя шаблона, в котором будет лежать HTML
    context_object_name = 'news'  # имя списка!!, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = News.objects.order_by('-dateCreation')
    ordering = ['-dateCreation']
    paginate_by = 10

    permission_required = 'newsapp.view_news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем фильтр в контекст
        return context


class NewsDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = News
    template_name = 'newsapp/note.html'
    context_object_name = 'note'

    permission_required = 'newsapp.view_news'


class NewsAddList(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'newsapp/newsAdd.html'
    form_class = NewsForm

    permission_required = 'newsapp.add_news'
    #права = приложение.действие_модель - а почему модель с маленькой буквы?
    # тем не менее permission_required = ('<app>.<action>_<model>', '<app>.<action>_<model>'...)

class NewsEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'newsapp/newsEdit.html'
    form_class = NewsForm
    model = News  # модель всё та же, но здесь мы хотим получать детали конкретно отдельного товара
    context_object_name = 'note'

    permission_required = 'newsapp.change_news'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'newsapp/newsDelete.html'
    context_object_name = 'note'
    queryset = News.objects.all()
    success_url = '/news/'

    permission_required = 'newsapp.delete_news'

class CategoryListView(ListView):
    model = News
    template_name = 'newsapp/category_list.html'

    # имя по которому мы будем обращатся к квери сету новостей в шаблоне
    context_object_name = 'category_news_list'
    # вот этой переменной чуть повыше мы обращаемся когда говорим иф ньюс - тогда заметок либо нет, либо говорим сколько штук и потом
    # перебираем в цикле и выдаем по одной заметке на строку таблицы шаблона обращаясь к записям в полях

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        #передаем мктоду404 модель и поле по которому фильтруем
        quryset = News.objects.filter(category=self.category).order_by('-dateCreation')
        return quryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

#@login_required - нам этого не надо, кто проник к нам в ньюсапп уже авторизован
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)  #строка добавляет юзера в поле сабскрайберс выбранной категории

    message = 'Вы подписались на рассылку новостей категории'

    return render(request, 'newsapp/subscribe.html', {'category':category, 'message': message})
    #после вызова функции - рендерим шаблон сабскрайб хтмл
    #  {'category':category, 'message': message}) - этот кусок аналогичен методу гет контекст ...
    #  дата - передаём значения в переменные для возможности вызова в шаблоне

def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)  #строка удолят юзера в поле сабскрайберс выбранной категории

    message = 'Вы отписались от рассылки новостей категории'
    return render(request, 'newsapp/unsubscribe.html', {'category':category, 'message': message})