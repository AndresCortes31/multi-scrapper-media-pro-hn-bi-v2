from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django_backend.views import ScraperViewSet

router = DefaultRouter()
router.register(r'scraper', ScraperViewSet, basename='scraper')

urlpatterns = [
    path('api/', include(router.urls)),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]