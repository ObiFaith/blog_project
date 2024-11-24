from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Blog(models.Model):
  title = models.CharField(max_length=255)
  content = CKEditor5Field(config_name='default')
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
  def __str__(self):
     # get the first 20 words of the title if title is not empty
    return " ".join(self.title.split()[:20]) if self.title else ""

class Comment(models.Model):
  comment = models.TextField()
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')

  def __str__(self):
    # get the first 20 words of the comment if comment is not empty
    return " ".join(self.comment.split()[:20]) if self.comment else ""
