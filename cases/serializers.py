from rest_framework import serializers
from .models import Case, CaseItem, UserInventory


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'name', 'image', 'price']


class CaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseItem
        fields = ['id', 'case', 'name', 'image', 'rarity', 'chance', 'price']
        read_only_fields = ['case']


class UserInventorySerializer(serializers.ModelSerializer):
    item = CaseItemSerializer()

    class Meta:
        model = UserInventory
        fields = ['id', 'user', 'item', 'received_at']
        read_only_fields = ['user', 'received_at']
