from django.urls import path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name='companies_list'),
    path('companies/<int:pk>', views.CompanyDetail.as_view(), name='companies_detail')
]