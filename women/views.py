from email import message

from django.contrib.auth import logout, login

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.edit import FormMixin


from .forms import *

from .utils import *

from django.core.mail import send_mail

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')




class AboutHome(DataMixin, ListView):
    model = About
    template_name = 'women/about.html'
    context_object_name = 'about'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        c_def = self.get_user_context(title="О сайте")
        return dict(list(context.items()) + list(c_def.items()))



class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление работы")
        return dict(list(context.items()) + list(c_def.items()))

class WorkHome(ListView):
    model = Work
    template_name = 'women/work.html'
    context_object_name = 'work'
    extra_context = {'title': 'Готовые работы'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


def show_work_one(request, work_id):
    work_one = get_object_or_404(Work, id=work_id)
    images = Images.objects.all()

    return render(request, 'women/work_one.html', {
        'work_one': work_one,
        'images': images,
        'menu': menu,

    })




class ContactCreate(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'women/contact.html', context={
            'form': form,
            'title': 'Написать мне',
            'menu': menu,
        })

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, ['kostianlomit@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'women/contact.html', context={
            'form': form,
            'menu': menu,
        })



class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'women/success.html', context={
            'title': 'Спасибо',
            'menu': menu,
        })




def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(FormMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = CommentForm

    success_url = 'Коментарий успешно создан'
    def get(self, request, *args, **kwargs):
        comment_form = CommentForm()
        return render(request, 'women/post.html', context={
            'comment_form':comment_form,
            'menu': menu,
        })

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            post = self.get_object()
            email = self.request.user
            comment_form.save()
            return render(request, 'women/post.html', context={
                ' comment_form':  comment_form,
                'email': email,
                'post': post,
                'menu': menu,
            })






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

