from django.contrib import admin
from .models import *
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogAdminForm(forms.ModelForm):
  content = forms.CharField(widget=CKEditor5Widget(config_name='default'))
  class Meta:
    model = Blog
    fields = '__all__'

class BlogAdmin(admin.ModelAdmin):
  form = BlogAdminForm

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)