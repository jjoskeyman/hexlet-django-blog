from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views import View
from .forms import *
from .models import *
from django.db.models import Q

#
# import os
#
# SECRET_KEY = os.getenv('SECRET_KEY')
# DEBUG = os.getenv('DEBUG', False)

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

articles_list = [
    {'id': 1, 'title': '"How to foo?"', 'author': 'F. BarBaz'},
    {'id': 2, 'title': '"Force 101"', 'author': 'O-W. Kenobi'},
    {'id': 3, 'title': '"Top 10 skyscrapers"', 'author': 'K. Kong'},
    {'id': 4, 'title': '"Top 10 skyscrapers (jp. edition)"', 'author': 'K. Godzilla'},
    {'id': 5, 'title': '"5 min recepies"', 'author': 'H. Lector'},
]


# def index(request):
#     posts = Women.objects.all()[:3]
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)
class IndexView(View):

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')
        if search_query:
            posts = Women.objects.filter(Q(title__icontains=search_query))
        else:
            posts = Women.objects.all()

        context = {
            'posts': posts,
            'menu': menu,
            'title': 'Главная страница',
            'cat_selected': 0,
        }
        return render(request, 'women/index.html', context=context)


@require_http_methods(['GET', 'POST'])
def articles(request):
    if request.method == 'POST':
        article = {
            'id': int(request.POST['id']),
            'title': request.POST['title'],
            'author': request.POST['author']
        }
        articles.append(article)
    return render(request, 'articles/index.html', context={'articles_list': articles_list})


@require_http_methods(['GET'])
def article_get(request, article_id):
    article = next((a for a in articles_list if a['id'] == article_id), None)
    if not article:
        raise Http404()
    return render(request, 'articles/article.html', context={'articles_list': articles_list})


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/add_page.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    cat = Category.objects.filter(slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat[0].id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat[0].id,
    }

    return render(request, 'women/index.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound(
        """<h1>
        There are not the page you're looking for. Come <a href="{% url 'home" %}">Home</a>, padawan!
        </h1>"""
    )
