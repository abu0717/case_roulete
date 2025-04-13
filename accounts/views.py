from decimal import Decimal, InvalidOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import User



class TelegramSimpleAuthView(APIView):
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username")
        referer_id = request.data.get("referer_id")

        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=400)

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"username": username}
        )

        if created and referer_id:
            try:
                referer = User.objects.get(telegram_id=referer_id)
                user.referer = referer
                user.save()
                referer.add_balance(500)
            except User.DoesNotExist:
                pass

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "telegram_id": telegram_id,
                "username": user.username,
                "referred_by": user.referer.telegram_id if user.referer else None
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
