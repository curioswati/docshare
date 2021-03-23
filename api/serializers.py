from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('doc_id', 'doc', 'name', 'editor', 'created_at')

    def get_name(self, obj):
        file_name = ''
        if obj.doc and hasattr(obj.doc, 'name'):
            file_name = obj.doc.name
        return file_name

    def get_created_at(self, obj):
        return obj.created_at
