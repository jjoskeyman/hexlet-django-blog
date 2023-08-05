from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render

TEAM = [
    {'name': 'Yoda', 'position': 'CEO'},
    {'name': 'Obi-Wan Kenobi', 'position': 'Senior Developer'},
    {'name': 'Anakin Skywalker', 'position': 'Junior Developer'},
    {'name': 'Jar Jar Binks', 'position': 'Trainee'},
]
articles_list = [
    {'id': 1, 'title': '"How to foo?"', 'author': 'F. BarBaz'},
    {'id': 2, 'title': '"Force 101"', 'author': 'O-W. Kenobi'},
    {'id': 3, 'title': '"Top 10 skyscrapers"', 'author': 'K. Kong'},
    {'id': 4, 'title': '"Top 10 skyscrapers (jp. edition)"', 'author': 'K. Godzilla'},
    {'id': 5, 'title': '"5 min recepies"', 'author': 'H. Lector'},
]


def index(request):
    return render(request,
                  'index.html',
                  )


def articles(request):
    return render(request,
                  'articles/index.html',
                  context={'articles_list': articles_list},
                  )


def about(request):
    return render(request,
                  'about.html',
                  context={'TEAM': TEAM},
                  )


def categories(request):
    if request.GET:
        print(request.GET)

    return HttpResponse(f"<h1>Статьи по категориям:</h1>")


def archive(request, year):
    if int(year) > 2020:
        return redirect('main_page', permanent=True)

    return HttpResponse(f"<h1>Архив по годам:</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Такая страница не найдена!</h1>')
