from django.shortcuts import redirect
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from .Mixin import *
from .forms import *
from .models import *
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.db.models import Q # для поска по нескольким полям

def posts(request):
    name = "Zoahn" # Хотим какието данные передать в контекст, тут переменную name
    names = ["kolia", "Vasia", "Petya", "Gora"] # передаем список в контекст и обрабатываем там цыклом шаблонизатора
    return render(request, "blog/post_list.html", context={"name": name, "names": names}) # request, шаблон, контекст

class MyListViewPost(ListView):

    model = Post
    template_name = "blog/post_list.html"


    def dispatch(self, request, *args, **kwargs):  # dispath определяет с каким запросом к нам прилетел запрос
        # Создаем переменную в которую кладем весь масив request.GET, а именно даннные которые пришли от пользователя в строке запроса,
        # будем с request.GET брать наш search и sort
        self.form = FormSearch(request.GET)
        # метод проверяет соответствуют ли данные той форме которую мы прописали, после чего можем оперировать таким атрибутом как cleaned_data
        self.form.is_valid()
        #
        self.search = Post(request.POST or None)  # Создали переменную для работы с POST, используется когда fprm.modelform
        return super(MyListViewPost, self).dispatch(request, *args, **kwargs)  # после чего вызываем super, что бы функция работала стандартно

    # def get_queryset(self):  # метод get_queryset, который берет текущую модель и выгребает все
    #     queryset = Post.objects.all()
    #
    #     # после вызова метода is_valid, заполняется атрибут cleaned_data, с него можем вытащить search,
    #     if self.form.cleaned_data.get("search"):  # Проверям засабмичен ли с формы search
    #         queryset = queryset.filter(title__icontains=self.form.cleaned_data["search"]) # если да, то фильтруем
    #
    #     if self.form.cleaned_data.get("sort"):  #
    #         queryset = queryset.order_by(self.form.cleaned_data["sort"])  # сортирум с помощью order_by по полю sort, проверили что оно есть
    #     return queryset  # можем переопредилить что бы выгребал последние [:4]

    """Можем переопредилить метод get_context_data - ето метод который вызывается у любого класса View и кторый составляет словарик
        отправляющийся в шаблон для рендера"""

    def get_context_data(self, **kwargs):

        queryset = Post.objects.all()

        if self.form.cleaned_data.get("search"):  # Проверям засабмичен ли с формы search
            # при поске можно сортировать по нескольким полям, но запятая ето как and, поиск будет осуществлен, с условием чтобы запрос был
            # найден одновременно в двух полях, для отдельного поиска нужно использовать класс Q, указав опера (| или)
            queryset = queryset.filter(Q(title__icontains=self.form.cleaned_data["search"]) | Q(body__icontains=self.form.cleaned_data["search"])) # если да, то фильтруем
        if self.form.cleaned_data.get("sort"):  #
            queryset = queryset.order_by(self.form.cleaned_data["sort"])


        paginator = Paginator(queryset, 3)  # сортируем по 3 обьекта в quryset
        page_number = self.request.GET.get("page")
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = "?page={}".format(page.previous_page_number())
        else:
            prev_url = ""

        if page.has_next():
            next_url = "?page={}".format(page.next_page_number())
        else:
            next_url = ""

        context = super(MyListViewPost, self).get_context_data(**kwargs)  # вызываем метод у родителя и добавляем контекст который нужен
        context["form"] = self.form  # добавляем нашу форму, кторая потом доступна в шаблоне
        context["search"] = self.search  # добавляем нашу форму, кторая потом доступна в шаблоне
        context["page"] = page
        context["is_paginated"] = is_paginated
        context["prev_url"] = prev_url
        context["next_url"] = next_url
        context["context"] = context
        return context




# def posts_list(request):
#     queryset = Post.objects.all() # взяли все обьекты в пост модели
#     paginator = Paginator(queryset, 2) # сортируем по 3 обьекта в quryset
#     page_number = request.GET.get("page", 1)
#     page = paginator.get_page(page_number)
#
#     is_paginated = page.has_other_pages()
#
#     if page.has_previous():
#         prev_url = "?page={}".format(page.previous_page_number())
#     else:
#         prev_url = ""
#
#     if page.has_next():
#         next_url = "?page={}".format(page.next_page_number())
#     else:
#         next_url = ""
#
#     context = {
#         "page": page,
#         "is_paginated": is_paginated,
#         "prev_url":prev_url,
#         "next_url":next_url,
#     }
#
#     return render(request, "blog/post_list.html", context=context)


# __iexact  - точное совпадение не чуствителен к регистру
# __contains - совпадение где есть искомое слово, и так как может быть пару таких обьектов, используем filter, он возвращает queryset

class MyListViewTag(ListView):

    model = Tag
    template_name = "blog/tag_list.html"

    def get_context_data(self, **kwargs):
        queryset = Tag.objects.all()
        context = super(MyListViewTag, self).get_context_data(**kwargs)
        context["tag_query"] = queryset
        return context

# def tag_list(request):
#     queryset = Tag.objects.all()
#     return render(request, "blog/tag_list.html", context={"tag_query": queryset})


class PostDetailView(DetailView):

    model = Post
    template_name = "blog/postdetail.html"

    # def get(self, request,  pk, **kwargs):
    #     post = self.model.objects.get(pk__iexact=pk)
    #     return render(self.request, self.template_name , context={self.model.__name__.lower(): post, "admin_n": post, 'True': True})

# class MyMixin:
#     model = None
#     template_name = None
#
# # eсли обратится к посту который не существует, то получим исключение а не ошибку 404, а нам нужна именно 404, потому тут его используем
#     def get(self, request, pk): # Метод get_object_or_404 имеет конструкцию (try, except) в try проверяет наличие slug в queryset
#                                   # (post = Post.objects.get(slug__iexact=slug)), если не находит то except - (ошибка 404)
#         obj = get_object_or_404(self.model, pk__iexact=pk)
#         return render(request, self.template_name, context={self.model.__name__.lower(): obj, "admin_n": obj, 'True': True})


# def post_detail(request, slug):
#     post = Post.objects.get(slug__iexact=slug) # вытаскиваем обьект с queryset где slug точно равно slug в любом регистре,
#                                             # через него обращаемся к его полям, а через url который обрабатывает Post_detail можем сделать ссылку
#     return render(request, "blog/postdetail.html", context={"post_detail" : post})
    # после урла в шаблоне обязательно в цыкле подставить - slug=post.slug, выбирало нужный slug и url переходил на него

# def tag_detail(request, slug):
#     tag = Tag.objects.get(slug__iexact=slug) # вытаскиваем обьект с queryset где slug точно равно slug в любом регистре,
#                                             # через него обращаемся к его полям, а через url который обрабатывает Post_detail можем сделать ссылку
#     return render(request, "blog/tagdetail.html", context={"tag_detail" : tag})
    # после урла в шаблоне обязательно в цыкле подставить - slug=post.slug, выбирало нужный slug и url переходил на него

# LoginRequiredMixin - с помощью него блокируем доступ к страницам со строки браузера
# class Post_detail(MyMixin, View): # Теперь нужно переопредилить у сласса View метод get, опредилили его в Mixin.py
#     model = Post # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
#     template_name = "blog/postdetail.html" # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
#     raise_exception = False


class TagDetailView(DetailView):

    model = Tag
    template_name = "blog/tagdetail.html"

    # def get(self, request,  pk, **kwargs):
    #     tag = self.model.objects.get(pk__iexact=pk)
    #     return render(self.request, self.template_name , context={self.model.__name__.lower(): tag, "admin_n": tag, 'True': True})


# class Tag_detail(MyMixin, View):
#     model = Tag # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
#     template_name = "blog/tagdetail.html" # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None


class TagCreate(LoginRequiredMixin,MixCreate, View): # тут мы долны принять запрос от пользователя Get и сохранить то что он переда Post, отработать 2 функции
    form = TagForm
    template_name = "blog/tag_create.html"
    raise_exception = True

    # def get(self, request):
    #     form = TagForm() # создали екземпляр класса формы TagForm
    #     return render(request, "blog/tag_create.html", context={"form":form}) # передаем форму в контекст
    #
    # def post(self, request):
    #     related_form = TagForm(request.POST)# создаем екземпляр класса TegForm, куда передаем подсловарь QuerydDict в конструктор
    #
    #     if related_form.is_valid(): # если форма валидная
    #         new_tag = related_form.save() # то сохраняем как новый экземпляр класса
    #         return redirect(new_tag) # и реверсим на ету форму, передав туда наш сохраненный экземпляр
    #     return render(request, "blog/tag_create.html", context={"form": related_form})
    #     # если форма не валидна то мы должны отобразить форму с теми данными которые он запонил и сообщить об ошибке

class TagUpdate(LoginRequiredMixin,MixUpdate, View):
    model = Tag
    form = TagForm
    template_name = "blog/tag_update_form.html"
    raise_exception = True

    # def get(self, request, pk):
    #     tag = Tag.objects.get(pk__iexact=pk) # tag ето наш экземпляр который мы вытянули с БД
    #     related_form = TagForm(instance=tag)  # создали новый екземпляр класа Form и в конструктор передали наш обьект c помощью instance
    #     return render(request, "blog/tag_update_form.html", context={"form": related_form, "tag": tag})
    #
    # def post(self, request, pk):
    #     tag = Tag.objects.get(pk__iexact=pk) # tag ето наш экземпляр который мы вытянули с БД
    #     related_form = TagForm(request.POST, instance=tag)  # создали новый екземпляр класа Form и в конструктор передали наш обьект c помощью instance, берем из реквеста
    #
    #     if related_form.is_valid():
    #         update_tag = related_form.save()  # то сохраняем как новый экземпляр класса
    #         return redirect(update_tag)  # и реверсим на ету форму, передав туда наш сохраненный экземпляр
    #     return render(request, "blog/tag_update_form.html", context={"form": related_form, "tag": tag})

"""создание через 3 строчки"""
class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_create.html"
    fields = ['title', "body"]

    # def get(self, request):
    #     form = self.form() # создали екземпляр класса формы TagForm
    #     return render(request, self.template_name, context={"form":form}) # передаем форму в контекст
    #
    # def post(self, request):
    #     related_form = self.form(request.POST)# создаем екземпляр класса TegForm, куда передаем подсловарь QuerydDict в конструктор
    #
    #     if related_form.is_valid(): # если форма валидная
    #         new_tag = related_form.save() # то сохраняем как новый экземпляр класса
    #         return redirect(new_tag) # и реверсим на ету форму, передав туда наш сохраненный экземпляр
    #     return render(request, self.template_name, context={"form": related_form})
    #     # если форма не валидна то мы должны отобразить форму с теми данными которые он запонил и сообщить об ошибке



# class PostCreate(LoginRequiredMixin,MixCreate, View):
#     form = PostForm
#     template_name = "blog/post_create.html"
#     raise_exception = True

"""Удаление через 3 строчки"""
class PostUpdateViwe(UpdateView):
    model = Post
    fields = ["title",'body']
    #template_name_suffix = '_update_form'
    template_name = "blog/post_update_form.html"



# class PostUpdate(LoginRequiredMixin,MixUpdate,View):
#     model = Post
#     form = PostForm
#     template_name = "blog/post_update_form.html"
#     raise_exception = True

    # def get(self, request, pk):
    #     post = Post.objects.get(pk__iexact=pk) # tag ето наш экземпляр который мы вытянули с БД
    #     related_form = PostForm(instance=post)  # создали новый екземпляр класа Form и в конструктор передали наш обьект c помощью instance
    #     return render(request, "blog/post_update_form.html", context={"form": related_form, "post": post})
    #
    # def post(self, request, pk):
    #     post = Post.objects.get(pk__iexact=pk) # tag ето наш экземпляр который мы вытянули с БД
    #     related_form = PostForm(request.POST, instance=post)  # создали новый екземпляр класа Form и в конструктор передали наш обьект c помощью instance, берем из реквеста
    #
    #     if related_form.is_valid():
    #         update_post = related_form.save()  # то сохраняем как новый экземпляр класса
    #         return redirect(update_post)  # и реверсим на ету форму, передав туда наш сохраненный экземпляр
    #     return render(request, "blog/post_update_form.html", context={"form": related_form, "tag": post})

class TagDelete(LoginRequiredMixin,MixDelete,View):

    model = Tag
    template_name = "blog/tag_del_form.html"
    redirect_url = "tag_list_url"
    raise_exception = True
    # def get(self, request, pk):
    #     tag = Tag.objects.get(pk__iexact=pk)
    #     return render(request, "blog/tag_del_form.html", context={"tag": tag})
    #
    # def post(self, request, pk):
    #     tag = Tag.objects.get(pk__iexact=pk)
    #     tag.delete()
    #     return redirect(reverse("post_list_url")) # куда вернет после удаления


"""для удаления достаточно указать 3 строки"""
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list_url')
    template_name = "blog/post_del_form.html"

# class PostDelete(LoginRequiredMixin,MixDelete, View):
#     model = Post
#     template_name = "blog/post_del_form.html"
#     redirect_url = "post_list_url"
#     raise_exception = True

    # def get(self, request, pk):
    #     post = Post.objects.get(pk__iexact=pk)
    #     return render(request, "blog/post_del_form.html", context={"post": post})
    #
    # def post(self, request, pk):
    #     post = Post.objects.get(pk__iexact=pk)
    #     post.delete()
    #     return redirect(reverse("post_list_url")) # куда вернет после удаления