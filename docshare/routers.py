from api.viewsets import DocumentViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'users', UserViewSet)
