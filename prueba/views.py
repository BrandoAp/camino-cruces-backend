from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class TestErrorView(APIView):
    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request):
        1 / 0
        return Response({"message": "No deberia llegar aqui"})
