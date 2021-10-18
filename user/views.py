from django.contrib.auth import logout, authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserCreateSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = serializer.data
        return Response(user, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request): # noqa
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email is None or password is None:
            return JsonResponse({"error": "Please provide email and password"})

        user = authenticate(username=email, password=password)

        if not user:  # Check if user exists
            return JsonResponse({"error": "Email or password incorrect"},
                                status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def get(self, request, format=None): # noqa
        # using Django built-in logout
        logout(request)
        return Response(status=status.HTTP_200_OK)
