from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)
router.register('review', views.ReviewViewSet)

urlpatterns = router.urls
