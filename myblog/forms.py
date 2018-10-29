from django import forms
from .models import *
from django.core.exceptions import ValidationError

# в моделях мы передавали в конструктор класса поля которые указали (title, bode и т.д.), в формах мы отступаем от этого общего поведения
# в формах мы должны передавать данные в конструктор которые мы берем из специального обьекта, из словаря который наз. clean_data
class TagForm(forms.ModelForm):
    #title = forms.CharField(max_length=50)  # это input
    #slug = forms.SlugField(max_length=50)

    class Meta:
        model = Tag
        fields = ["title", "slug"]


    # для того что бы в url который принимает именое значение blog/<slug> не попал create как slug, при переходе на страницу blog/create
    # нам нужно сделать проверку, с помошью метода clean_slug (slug тут потму что проверям slug, стаил такой)
    def clean_slug(self):

        new_slug = self.cleaned_data["slug"].lower()

        if new_slug == "create": # делаем проверку на create в slug
            raise ValidationError("slug не может быть create")
        if Tag.objects.filter(slug__iexact=new_slug).count():  # делаем проверку что бы поле не дублировалось
            raise ValidationError("Поле slug -  {} уже существует".format(new_slug))
        return new_slug


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "body", "slug" ,"tags_to_post"]

    def clean_post(self):

        new_post = self.cleaned_data["slug"].lower()

        if new_post == "create":
            raise ValidationError ("Post не может быть create")
        if Post.objects.filter(slug__iexact=new_post).count():
            raise ValidationError("Такой slug существует")
        return new_post


    # коментируем save, так как у ModelForm есть свой метод save

    # переопределяем мето save, который нам вернет (сохранит в базе) поля title и slug но уже со словаря cleaned_data
    #def save(self):
        #new_tag = Tag.objects.create(title=self.cleaned_data["title"], slug=self.cleaned_data["slug"])
        #return new_tag


    # from blog.form import TagForm
    # tf = TegForm()     создал екземпляр класса     <TagForm bound=False, valid=Unknown, fields=(title;slug)>   bound=False - ввел пользователь что то или нет
    # dir(tf)    список атрибутов сщзданого нами обьекта
    # from blog.form import TagForm
    # tf = TegForm()     создал екземпляр класса     <TagForm bound=False, valid=Unknown, fields=(title;slug)>   bound=False - ввел пользователь что то или нет

    # dir(tf) обратились к атрибутам обьекта
    # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__',
    # '__gt__', '__hash__', '__html__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
    # '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_bound_fields_cache',
    # '_clean_fields', '_clean_form', '_errors', '_html_output', '_post_clean', 'add_error', 'add_initial_prefix', 'add_prefix', 'as_p',
    # 'as_table', 'as_ul', 'auto_id', 'base_fields', 'changed_data', 'clean', 'data', 'declared_fields', 'default_renderer', 'empty_permitted',
    # 'error_class', 'errors', 'field_order', 'fields', 'files', 'full_clean', 'get_initial_for_field', 'has_changed', 'has_error', 'hidden_fields',
    # 'initial', 'is_bound', 'is_multipart', 'is_valid', 'label_suffix', 'media', 'non_field_errors', 'order_fields', 'prefix', 'renderer',
    # 'use_required_attribute', 'visible_fields']

    # tf.is_bound    False    проверяем передал ли что то пользователь в форму
    # tf.is_valid() False     так как is_bound - False, то и is_valid() False
    # tf.errors {}  тоже пустой так как мы не передали никаких данных
    # d = {"title":"", "slug":""}  создали словарь, с пустыми строками
    # tf=TagForm(d) # снова создаю экземпляр, но на етот раз передаю словарь
    # # tf.is_bound    True    проверяем передал ли что то пользователь в форму, сейчас передал
    # tf.is_valid() False
    # tf.errors   {'title': ['Обязательное поле.'], 'slug': ['Обязательное поле.']}    видим что есть обязательные поля
    # # dir(tf) если снова обратимся к атрибутам, то видим что появился cleaned_date
    # tf.cleaned_data     выдаст пустой словарь  {} -  очищенные данные, потому что у нас заполнена форма tf.is_bound - True, и вызвали метод is_valid(),
    # в етот момент создается словарь cleaned_data, если бы is_valid был бы True, ети бы данные были бы заполнены
    # d = {"title":"fack", "slug":"me"}
    # tf = TagForm(d)
    # tf.is_bound     True
    # tf.is_valid()   True  - так как передали уже не пустую строку
    # tf.cleaned_data   при вызове видим что в словаре данные которые передал пользователь   {'title': 'fack', 'slug': 'me'}
    # tf.cleaned_data  содержит очищиные данные, и именно данные из егото словаря мы должны использовать для создания моделей



    # from myblog.models import Tag

    # tag = Tag(title=tf.cleaned_data["title"], slug=tf.cleaned_data["slug"])  создал новый обьект в models.tag и передал данные с обьекта Tegform
    # который у нас tf и с его словаря cleaned_data

    # В общем виде валидация данных (проверка) и их очистка выглядит следующим образом:
    # django вызывает метод is_valid который если True, последовательно вызывает clean методы, всей формы и отдельных полей
    # если все проверено и валидировано, то они и помещаются в словарь cleaned_data, если что то не то, то исключение Validatioerrors