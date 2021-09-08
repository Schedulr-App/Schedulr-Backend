from django.urls import path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name='companies_list'),
    path('companies/<int:pk>', views.CompanyDetail.as_view(), name='companies_detail'),
    path('shifts/', views.shift_list, name='shifts_list'),
    path('shifts/<int:pk>', views.shift_detail, name='shift_detail')
]