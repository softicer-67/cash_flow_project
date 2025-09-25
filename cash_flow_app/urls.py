from django.urls import path
from . import views


urlpatterns = [
    path('', views.cash_flow_list, name='cash_flow_list'),
    path('create/', views.cash_flow_create, name='cash_flow_create'),
    path('edit/<int:pk>/', views.cash_flow_edit, name='cash_flow_edit'),
    path('delete/<int:pk>/', views.cash_flow_delete, name='cash_flow_delete'),
    path('reference-books/', views.reference_books, name='reference_books'),
    path('load-categories/', views.load_categories, name='load_categories'),
    path('load-subcategories/', views.load_subcategories, name='load_subcategories'),
]
