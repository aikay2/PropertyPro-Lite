from django.urls import path
from . import views 

urlpatterns = [
    path('property/', views.PropertyAPIView.as_view(), name="properties"),
    path('property/<int:pk>/', views.SinglePropertyAPIView.as_view(), name="property-detail"),
    path('property/<int:pk>/sold/', views.PropertyStatusAPIView.as_view(), name="property-status-update"),
    path('property/<int:pk>/flag/', views.FlagCreateView.as_view(), name="flags-create"),
    path('property/flags/', views.FlagListView.as_view(), name="flags-list"),
    path('property/<int:pk>/flags/', views.FlagPropertyList.as_view(), name="property-flags-list"),
    path('property/flags/<int:pk>/', views.FlagDetailView.as_view(), name="flag-detail"),
]
