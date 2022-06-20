from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, Tag
from .serializers import TaskSerializer, TagSerializer
from .services import get_all_or_filter,get_notice_time
from .permissions import IsOwnerOrReadOnly
from .tasks import send_notice
from rest_framework.decorators import action


class TaskViewSet(viewsets.ModelViewSet):
    """ Обработка запросов, связанных с Task """
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = get_all_or_filter(Task, user=self.request.user)
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = get_all_or_filter(Task,
                                         user=self.request.user,
                                         tags__tag_name=tag)
        return queryset

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action != 'list':
            permission_classes.append(IsOwnerOrReadOnly)
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        send_notice.apply_async((self.request.user.email, serializer.data),
                                countdown=get_notice_time(serializer.data['deadline']))
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def completed(self, request):
        queryset = get_all_or_filter(Task,
                                     user=request.user,
                                     is_completed=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListTagView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """ Просмотр,добавление,удаление Тэгов"""
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_all_or_filter(Tag, user=self.request.user)

