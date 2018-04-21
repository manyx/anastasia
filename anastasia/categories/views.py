from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework import parsers, renderers, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from categories.models import Category
from categories.serializers import *
from django.http import Http404


class CategoriesList(APIView):
    """
    Post Categories or List all Categories
    """
    serializer_class = CategorySerializer

    def recursive_save(self, node, parent):
        if parent:
            serializer = CategorySerializer(data={'name': node['name'], 'parent': parent})
        else:
            serializer = CategorySerializer(data={'name': node['name']})
        if serializer.is_valid():
            category = serializer.save()
            category_id = category.id
            if 'children' in node:
                for item in node['children']:
                    self.recursive_save(item, category_id)
            return True
        return False

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if self.recursive_save(request.data, False):
            return Response(True, status=status.HTTP_201_CREATED)
        else:
            return Response(False, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    """
    Retrieve, update or delete a Category instance.
    """
    serializer_class = CategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
