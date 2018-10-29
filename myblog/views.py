from django.shortcuts import redirect
from django.views.generic import View, CreateView
from .Mixin import *
from .forms import *
from .models import *
from django.shortcuts import render
# Create your views here.


def posts(request):
    name = "Zoahn" # Хотим какието данные передать в контекст, тут переменную name
    names = ["kolia", "Vasia", "Petya", "Gora"] # передаем список в контекст и обрабатываем там цыклом шаблонизатора
    return render(request, "blog/post_list.html", context={"name": name, "names": names}) # первый аргумент request,
                                                                                      # второй - путь к шаблону,
                                                                                      # потом можем передать контекст

def posts_list(request):
    queryset = Post.objects.all()
    return render(request, "blog/post_list.html", context={"post_query": queryset})

# __iexact  - точное совпадение не чуствителен к регистру
# __contains - совпадение где есть искомое слово, и так как может быть пару таких обьектов, используем filter, он возвращает queryset

def tag_list(request):
    queryset = Tag.objects.all()
    return render(request, "blog/tag_list.html", context={"tag_query": queryset})



def post_detail(request, slug):
    post = Post.objects.get(slug__iexact=slug) # вытаскиваем обьект с queryset где slug точно равно slug в любом регистре,
                                            # через него обращаемся к его полям, а через url который обрабатывает Post_detail можем сделать ссылку
    return render(request, "blog/postdetail.html", context={"post_detail" : post})
    # после урла в шаблоне обязательно в цыкле подставить - slug=post.slug, выбирало нужный slug и url переходил на него

def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug) # вытаскиваем обьект с queryset где slug точно равно slug в любом регистре,
                                            # через него обращаемся к его полям, а через url который обрабатывает Post_detail можем сделать ссылку
    return render(request, "blog/tagdetail.html", context={"tag_detail" : tag})
    # после урла в шаблоне обязательно в цыкле подставить - slug=post.slug, выбирало нужный slug и url переходил на него



class Post_detail(MyMixin, View): # Теперь нужно переопредилить у сласса View метод get, опредилили его в Mixin.py
    model = Post # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
    template_name = "blog/postdetail.html" # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None



class Tag_detail(MyMixin, View):
    model = Tag # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
    template_name = "blog/tagdetail.html" # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None

class TagCreate(View): # тут мы долны принять запрос от пользователя Get и сохранить то что он переда Post, отработать 2 функции

    def get(self, request):
        form = TagForm() # сщздали екземпляр класса
        return render(request, "blog/tag_create.html", context={"form":form}) # передаем форму в контекст

    def post(self, request):
        sviazannayaforma = TagForm(request.POST)# создаем екземпляр класса TegForm, куда передаем подсловарь QuerydDict

        if sviazannayaforma.is_valid(): # если форма валидная
            new_tag = sviazannayaforma.save() # то сохраняем
            return redirect(new_tag) # и реверсим на ету форму, передав туда наш экземпляр
        return render(request, "blog/tag_create.html", context={"form": sviazannayaforma})
        # если форма не валидна то мы должны отобразить форму с теми данными которые он запонил и сообщить об ошибке
