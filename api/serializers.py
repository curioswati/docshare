from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Document


# Ref: https://nemecek.be/blog/23/how-to-createregister-user-account-with-django-rest-framework-api
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    # Ref: https://stackoverflow.com/a/34428116
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class DocumentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    editor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                                many=True, required=False)

    class Meta:
        model = Document
        fields = ('doc_id', 'doc', 'name', 'editor', 'created_at')
        extra_kwargs = {'doc': {'required': False}}

    def get_name(self, obj):
        file_name = ''
        if obj.doc and hasattr(obj.doc, 'name'):
            file_name = obj.doc.name
        return file_name

    def get_created_at(self, obj):
        return obj.created_at
