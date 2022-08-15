from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name='dispatch')
class Recipe(APIView):
    def get(self, request):
        try:
            customer_uuid = request.META['HTTP_CUSTOMER_UUID']
            recipe_id = request.GET.get('recipe_id')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_id': recipe_id,
        }