import random
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from transaction.models import Transaction
from .models import Case, CaseItem, UserInventory
from .serializers import CaseSerializer, CaseItemSerializer, UserInventorySerializer


# Create your views here.

class CaseListView(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]


class CaseDetailView(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class CaseItemListView(generics.ListAPIView):
    queryset = CaseItem.objects.all()
    serializer_class = CaseItemSerializer
    permission_classes = [IsAuthenticated]


class CaseItemDetailView(generics.RetrieveAPIView):
    queryset = CaseItem.objects.all()
    serializer_class = CaseItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class UserInventoryListView(generics.ListAPIView):
    queryset = UserInventory.objects.all()
    serializer_class = UserInventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class UserInventoryDetailView(generics.RetrieveAPIView):
    queryset = UserInventory.objects.all()
    serializer_class = UserInventorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class OpenCaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        try:
            case = Case.objects.get(id=id)
        except Case.DoesNotExist:
            return Response({"error": "Case not found"}, status=404)

        if user.balance < case.price:
            return Response({"error": "Insufficient balance"}, status=400)

        items = list(case.items.all())
        if not items:
            return Response({"error": "No items in case"}, status=400)

        weights = [item.chance for item in items]
        dropped_item = random.choices(items, weights=weights, k=1)[0]
        user.spend_balance(case.price)

        Transaction.objects.create(
            user=user,
            transaction_type=Transaction.TransactionType.CASE_PURCHASE,
            amount=-case.price,
            item=dropped_item
        )

        return Response({"success": True, "item": CaseItemSerializer(dropped_item).data}, status=200)


class SellItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        if not item_id:
            return Response({'detail': 'item_id is required'}, status=400)

        try:
            item = CaseItem.objects.get(id=item_id)
        except CaseItem.DoesNotExist:
            return Response({'detail': 'Item not found'}, status=404)

        request.user.add_balance(item.price)

        Transaction.objects.create(
            user=request.user,
            transaction_type=Transaction.TransactionType.ITEM_DROP,
            amount=item.price,
            item=item
        )
        user_inventory = UserInventory.objects.filter(user=request.user, item=item).first()
        if user_inventory:
            user_inventory.delete()
        else:
            return Response({'detail': 'Item not found in inventory'}, status=404)
        return Response({'message': f"{item.name} sold for {item.price} ULA."}, status=200)


class KeepItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        if not item_id:
            return Response({'detail': 'item_id is required'}, status=400)

        try:
            item = CaseItem.objects.get(id=item_id)
        except CaseItem.DoesNotExist:
            return Response({'detail': 'Item not found'}, status=404)

        # Add to user inventory
        UserInventory.objects.create(user=request.user, item=item)

        return Response({'message': f"{item.name} added to inventory."}, status=200)
