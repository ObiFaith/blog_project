from .models import *
from .serializers import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def users(request, format=None):
  if request.method == 'GET':
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  pass

@api_view(['GET', 'PUT', 'DELETE'])
def user(request, id, format=None):
  pass

@api_view(['GET', 'POST'])
def blogs(request, format=None):
  if request.method == 'GET':
    # get blogs
    blogs = Blog.objects.all()
    # serialize blogs
    serializer = BlogSerializer(blogs, many=True)
    # return serializer data as response
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    # todo: authorize before adding blogs
    # deserialize and validate data from POST
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({ "error": "title, content, and user_id are all required"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def blog(request, id, format=None):
  try:
    blog = Blog.objects.get(pk=id)
  except Blog.DoesNotExist:
    return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = BlogSerializer(blog)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    # todo: authorize before updating a blog
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({ "error": "title, content and user_id are all required"}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    # todo: authorize before deleting a blog
    blog.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def comments(request, format=None):
  if request.method == 'GET':
    # get comments
    comments = Comment.objects.all()
    # serialize comments
    serializer = CommentSerializer(comments, many=True)
    # return serializer data as response
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    # deserialize and validate data from POST
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def comment(request, id, format=None):
  try:
    comment = Comment.objects.get(pk=id)
  except Comment.DoesNotExist:
    return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'PUT':
    # todo: only authorized users can modfiy a comment
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({ "error": "comment, blog_id and user_id are all required"}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    # todo: only authorized users can modfiy a comment
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
