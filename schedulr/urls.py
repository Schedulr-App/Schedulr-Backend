from django.urls import path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name='companies_list'),
    path('companies/<int:pk>', views.CompanyDetail.as_view(), name='companies_detail'),
    path('positions/', views.PositionList.as_view(), name='positions_list'),
    path('positions/<int:pk>', views.PositionDetail.as_view(), name='positions_detail'),
    path('shifts/', views.shift_list, name='shifts_list'),
    path('shifts/new', views.shift_create, name='shift_create'),
    path('shifts/update', views.shift_update, name='shift_update'),
    path('shifts/<int:pk>', views.shift_detail, name='shift_detail'),
    path('workforce/', views.user_list, name='user_list'),
]