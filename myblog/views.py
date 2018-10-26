from django.shortcuts import render
from .models import *

# Create your views here.


def posts(request):
    name = "Zoahn" # Хотим какието данные передать в контекст, тут переменную name
    names = ["kolia", "Vasia", "Petya", "Gora"] # передаем список в контекст и обрабатываем там цыклом шаблонизатора
    return render(request, "blog/index.html", context={"name": name, "names": names}) # первый аргумент request,
                                                                                      # второй - путь к шаблону,
                                                                                      # потом можем передать контекст

def posts_list(request):
    queryset = Post.objects.all()
    return render(request, "blog/index.html", context={"post_query": queryset})


# __iexact  - точное совпадение не чуствителен к регистру
# __contains - совпадение где есть какоето слово, и может быть пару таких обьектов, потому тут через filter, он возвращает кверисет
