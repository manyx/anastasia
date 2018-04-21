from django.contrib.auth.models import User, Group
from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, obj):
        serialized_data = super(CategorySerializer, self).to_representation(obj)

        # get children
        category_id = serialized_data.get('id')
        children_entries = Category.objects.filter(parent=category_id)
        children_serializer = CategoryMemberSerializer(children_entries, many=True)

        # get siblings
        parent = serialized_data.get('parent')
        siblings_entries = Category.objects.filter(parent=parent).exclude(id=category_id)
        siblings_serializer = CategoryMemberSerializer(siblings_entries, many=True)

        # get parents
        parents = []
        if parent:
            parent_entry = Category.objects.get(pk=parent)
            parent_serializer = CategoryMemberSerializer(parent_entry)
            parents.append(parent_serializer.data)
            next_parent = parent_entry.parent
            # import pdb; pdb.set_trace()

            while (next_parent):
                parent_entry = Category.objects.get(pk=next_parent.id)
                parent_serializer = CategoryMemberSerializer(parent_entry)
                parents.append(parent_serializer.data)
                next_parent = parent_entry.parent

        if len(parents) > 0:
            serialized_data['parents'] = parents

        serialized_data['children'] = children_serializer.data
        serialized_data['siblings'] = siblings_serializer.data

        serialized_data.pop('parent')
        return serialized_data


class CategoryMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
