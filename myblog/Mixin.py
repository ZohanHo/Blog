from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

class MyMixin:
    model = None
    template_name = None

# eсли обратится к посту который не существует, то получим исключение а не ошибку 404, а нам нужна именно 404, потому тут его используем
    def get(self, request, pk): # Метод get_object_or_404 имеет конструкцию (try, except) в try проверяет наличие slug в queryset
                                  # (post = Post.objects.get(slug__iexact=slug)), если не находит то except - (ошибка 404)
        obj = get_object_or_404(self.model, pk__iexact=pk)
        return render(request, self.template_name, context={self.model.__name__.lower(): obj, "admin_n": obj, 'True': True}) # текущаяя модель, ее имя маленькими буквами


class MixCreate(): # тут мы долны принять запрос от пользователя Get и сохранить то что он переда Post, отработать 2 функции
    form = None
    template_name = None

    def get(self, request):
        form = self.form() # создали екземпляр класса формы TagForm
        return render(request, self.template_name, context={"form":form}) # передаем форму в контекст

    def post(self, request):
        related_form = self.form(request.POST)# создаем екземпляр класса TegForm, куда передаем подсловарь QuerydDict в конструктор

        if related_form.is_valid(): # если форма валидная
            new_tag = related_form.save() # то сохраняем как новый экземпляр класса
            return redirect(new_tag) # и реверсим на ету форму, передав туда наш сохраненный экземпляр
        return render(request, self.template_name, context={"form": related_form})
        # если форма не валидна то мы должны отобразить форму с теми данными которые он запонил и сообщить об ошибке


class MixUpdate():
    model = None  # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
    form = None
    template_name = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk) # tag ето наш экземпляр который мы вытянули с БД
        related_form = self.form(instance=obj)  # создали новый екземпляр класа Form и в конструктор передали наш обьект c помощью instance
        return render(request, self.template_name, context={"form": related_form, self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk) # tag ето наш экземпляр который мы вытянули с БД
        related_form = self.form(request.POST, instance=obj)  # создали новый екземпляр класа Form и в конструктор передали наш обьект c помощью instance, берем из реквеста

        if related_form.is_valid():
            update_obj = related_form.save()  # то сохраняем как новый экземпляр класса
            return redirect(update_obj)  # и реверсим на ету форму, передав туда наш сохраненный экземпляр
        return render(request, self.template_name, context={"form": related_form, self.model.__name__.lower(): obj})


class MixDelete():
    model = None  # переопрелилили поле model в класе наследнике, тоесть тут, в базовом класе None
    template_name = None
    redirect_url = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk)
        return render(request, self.template_name, context={self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk__iexact=pk)
        obj.delete()
        return redirect(reverse(self.redirect_url)) # куда вернет после удаления