from django.urls import path, include, re_path
from .views import TaskViewSet, ListTagView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
appname = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
    path('tags', ListTagView.as_view(), name='tags'),
    path('tags/<int:pk>', ListTagView.as_view(), name='tag_detail'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    ]
