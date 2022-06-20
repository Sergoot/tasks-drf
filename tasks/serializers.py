from rest_framework import serializers
from .models import Task, Tag
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Задач """
    date_published = serializers.DateTimeField(read_only=True)
    deadline = serializers.DateField(required=True)
    tags = serializers.SlugRelatedField(
        many=True,
        queryset= Tag.objects.all(),
        slug_field='tag_name'
    )

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data['tags']
        validated_data.pop('tags')
        instance = Task.objects.create(**validated_data)
        for tag in tags:
            instance.tags.add(tag)
        return instance


class TagSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели Тэгов """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = '__all__'
