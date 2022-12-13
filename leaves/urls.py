from django.urls import path
from . import views

urlpatterns = [
    path('leaveDataDisplay/', views.leaveDataDisplay, name='leaveDataDisplay'),
    path('searchLeavesData/', views.searchLeavesData, name='searchLeavesData'),
    # path('searchLeavesData/', reasonEntry.searchLeavesData, name='searchLeavesData'),
    path('leaveTypeSelect/', views.leaveTypeSelect, name='leaveTypeSelect'),
    path('statusSelect/', views.statusSelect, name='statusSelect'),
    path('monthDataFilter/', views.monthDataFilter, name='monthDataFilter'),
    path('validateLeaves/', views.validateLeaves, name='validateLeaves'),
    path('applyLeavesData/', views.applyLeavesData, name='applyLeavesData'),
]