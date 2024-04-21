from django import forms
from news.models import Post
from django.core.exceptions import ValidationError


class PostFormArticles(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'postCategory', 'title', 'text', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("title")
        name = cleaned_data.get("text")

        if name == description:
            raise ValidationError(
                "Заголовок не должн быть идентичным тексту статьи."
            )

        return cleaned_data
