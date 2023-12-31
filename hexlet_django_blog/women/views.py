from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from .forms import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *


class IndexView(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


class About(DataMixin, ListView):
    model = Women
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О сайте")
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class PostFormEditView(DetailView):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        post = Women.objects.get(slug=slug)
        form = AddPostForm(instance=post)
        messages.success(request, 'Post edited successfully')
        return render(request, 'women/update.html', {'form': form, 'slug': slug})

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        post = Women.objects.get(slug=slug)
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'women/update.html', {'form': form, 'slug': slug})


class PostFormDeleteView(DeleteView):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        post = Women.objects.get(slug=slug)
        if post:
            post.delete()
        messages.success(request, 'Post delited successfully')
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["post"])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def page_not_found(request, exception):
    return HttpResponseNotFound(
        """<h1>
        There are not the page you're looking for. Come <a href="{% url 'home" %}">Home</a>, padawan!
        </h1>"""
    )
