from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .models import ShareData
from .serializers import ShareDataSerializer


@api_view(['GET', 'POST', 'DELETE'])
def sharedata(request):
    if request.method == 'GET':
        code = request.query_params.get('code', None)
        if code is None:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        data = ShareData.objects.all()
        try:
            data = data.get(Code=code)
        except ShareData.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        data_serializer = ShareDataSerializer(data)
        return JsonResponse(data_serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data_serializer = ShareDataSerializer(data=data)
        if data_serializer.is_valid():
            data_serializer.save()
            return JsonResponse(data_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        code = request.query_params.get('code', None)
        if code is None:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        try:
            data = ShareData.objects.get(Code=code).delete()
        except ShareData.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)