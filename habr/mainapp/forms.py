from django import forms
from .models import Article


class CreateArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'category', 'article_text']
        labels = {
            'title': 'Введите заголовок',
            'article_text': "Ваши мысли тут"
        }

    def __init__(self, *args, **kwargs):
        super(CreateArticleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
