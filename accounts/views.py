from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .serializers import ProfileSerializer
from .utils import verify_telegram_auth

# Create your views here.


User = settings.AUTH_USER_MODEL


class TelegramAuth(APIView):
    def post(self, request):
        init_data = request.data.get('init_data')
        if not init_data:
            return Response({"error": "Missing init_data"}, status=status.HTTP_400_BAD_REQUEST)
        if not verify_telegram_auth(init_data, settings.TELEGRAM_BOT_TOKEN):
            return Response({"error": "Invalid init_data"}, status=status.HTTP_400_BAD_REQUEST)

        from urllib.parse import parse_qs
        data = dict(parse_qs(init_data))
        telegram_id = data["id"][0]
        username = data.get("username", [None])[0]

        user, created = User.objects.get_or_create(telegram_id=telegram_id, defaults={"username": username})

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "telegram_id": telegram_id,
                "username": username,
                "created": created,
            }
        })


class AddBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Missing amount"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"error": "Amount must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.add_balance(amount)
        return Response({"message": f"{amount} ULA added successfully"}, status=status.HTTP_200_OK)


class GetProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return self.request.user
