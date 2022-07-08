from dataclasses import fields
from django import forms

from .models import Article

from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class ArticleForm(forms.ModelForm):
    
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows':20}
            )
    )
    class Meta:
        model = Article
        fields = '__all__'

"""
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "summary", "content", "tags", "featured", "thumbnail", "next_article", "previous_article", "status"]
        widgets = {"summary": forms.TextInput()}
"""