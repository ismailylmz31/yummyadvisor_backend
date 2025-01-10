from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .middlewares.auth_middleware import Auth0JSONWebTokenAuthentication


class AuthCheckView(APIView):
    def get(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]
        auth = Auth0JSONWebTokenAuthentication()
        user_info = auth.decode_jwt(token)
        return Response({"message": "Authenticated!", "user": user_info})
