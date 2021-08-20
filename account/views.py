from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import MyUser
from account.serializers import RegisterSerializer, CreateNewPasswordSerializer
from account.utls import send_activation_code


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('successfully registered', 201)


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = MyUser.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response('this user does not exist', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Ваш профиль активирован', 200)


class ForgotPasswordView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(email=user.email, activation_code=user.activation_code, status='reset_password')
        return Response('Активационный код для сброса пароля отправлен на почту', 200)


class CompleteResetPassword(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', 200)