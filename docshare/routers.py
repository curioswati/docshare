from api.viewsets import DocumentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet)
