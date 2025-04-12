from django.urls import path
from .views import (
    CaseListView,
    CaseDetailView,
    CaseItemListView,
    CaseItemDetailView,
    UserInventoryListView,
    UserInventoryDetailView,
    OpenCaseView,
    SellItemView,
    KeepItemView
)

urlpatterns = [
    path('cases/', CaseListView.as_view(), name='case-list'),
    path('case/<uuid:id>/', CaseDetailView.as_view(), name='case-detail'),
    path('case-items/', CaseItemListView.as_view(), name='case-item-list'),
    path('case-items/<uuid:id>/', CaseItemDetailView.as_view(), name='case-item-detail'),
    path('user-inventory/', UserInventoryListView.as_view(), name='user-inventory-list'),
    path('user-inventory/<uuid:id>/', UserInventoryDetailView.as_view(), name='user-inventory-detail'),
    path('case/<uuid:id>/open/', OpenCaseView.as_view(), name='open-case'),
    path('sell-item/<uuid:item_id>/', SellItemView.as_view(), name='sell-item'),
    path('keep-item/<uuid:item_id>/', KeepItemView.as_view(), name='keep-item'),
]
