from .models import *
from .serializers import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, get_user_model, authenticate, logout

User = get_user_model()

@api_view(['POST'])
def signup(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    user = User.objects.create_user(**serializer.validated_data)
    login(request._request, user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
  serializer = LoginSerializer(data=request.data)
  if serializer.is_valid():
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
      login(request._request, user)
      return Response({"message": "Logged in successfully!"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
  logout(request)
  return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def user(request, id, format=None):
  try:
    user = User.objects.get(pk=id)
  except User.DoesNotExist:
    return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == "GET":
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == "PUT":
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == "DELETE":
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

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
    if not request.user.is_authenticated():
      return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    # deserialize and validate data from POST
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"error": "title, content, and user_id are all required"}, status=status.HTTP_400_BAD_REQUEST)

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
    if not request.user.is_authenticated():
      return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "title, content and user_id are all required"}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    if not request.user.is_authenticated():
      return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
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
    if not request.user.is_authenticated():
      return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "comment, blog_id and user_id are all required"}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    if not request.user.is_authenticated():
      return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
