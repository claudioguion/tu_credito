from rest_framework.routers import DefaultRouter
from .views import CreditViewSet


router = DefaultRouter()
router.register(r"creditos", CreditViewSet, basename="credit")

urlpatterns = router.urls
