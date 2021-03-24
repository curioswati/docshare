from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_condition import condition

from .models import Document
from .serializers import DocumentSerializer, UserSerializer


def my_etag(request, *args, **kwargs):
    doc_id = kwargs.get('pk')
    instance = Document.objects.get(pk=doc_id)
    return str(instance.version)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    @condition(etag_func=my_etag)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # If the user is not owner and the document is being updated by owner
        # then the user must not get the document until updated.
        if request.user != instance.owner and 'If-Match' not in request.headers:
            return Response('Missing resource version in If-Match',
                            status=status.HTTP_428_PRECONDITION_REQUIRED)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
        serializer.save(owner=self.request.user, version=1)

    def perform_update(self, serializer):
        serializer.save(version=F('version') + 1)

    @condition(etag_func=my_etag)
    def update(self, request, *args, **kwargs):
        if 'If-Match' not in request.headers:
            return Response('Missing resource version in If-Match',
                            status=status.HTTP_428_PRECONDITION_REQUIRED)

        elif not request.headers.get('If-Match').startswith('"'):
            return Response('If-Match header value should be enclosed in double quotes.',
                            status=status.HTTP_412_PRECONDITION_FAILED)

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
