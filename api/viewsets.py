from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer, UserSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all documents owned by user.
        owned = self.request.user.documents.all()

        # Get all documents shared with user.
        can_access = Document.objects.filter(editor=self.request.user)

        return owned | can_access

    def create(self, request, *args, **kwargs):
        data = {key: value for key, value in request.data.items()}
        data['editor'] = User.objects.filter(
                                             username=request.data.get('editor')
                                             ).values_list('id', flat=True)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

    def update(self, request, *args, **kwargs):
        data = {key: value for key, value in request.data.items()}

        editor = request.data.get('editor')
        if editor:
            shared_with = request.data.get('editor').split()
            editors = User.objects.filter(username__in=shared_with).values_list('id', flat=True)
            if editors:
                data['editor'] = editors

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()
