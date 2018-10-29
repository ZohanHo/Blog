from django.shortcuts import render, get_object_or_404


class MyMixin:
    model = None
    template_name = None

# усли обратится к посту который не существует, то получим исключение а не ошибку 404, а нам нужна именно 404, потому тут его используем
    def get(self, request, slug): # Метод get_object_or_404 имеет конструкцию (try, except) в try проверяет наличие slug в queryset
                                  # (post = Post.objects.get(slug__iexact=slug)), если не находит то except - (ошибка 404)
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template_name, context={self.model.__name__.lower(): obj}) # текущаяя модель, ее имя маленькими буквами


