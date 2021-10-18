from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseViewSet(ModelViewSet):
    """Base ViewSet class inherited by view classes in other apps."""

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({"error": "Address already exists!"}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return JsonResponse({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return JsonResponse({"error": "Address already exists!"}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return JsonResponse({"error": e}, status=status.HTTP_400_BAD_REQUEST)
