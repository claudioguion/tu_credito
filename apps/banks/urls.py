from rest_framework.routers import DefaultRouter

from .views import BankViewSet


router = DefaultRouter()
router.register(r'bancos', BankViewSet, basename='bank')  # /api/bancos/

urlpatterns = router.urls
