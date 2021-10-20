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
    path('shifts/assign', views.shift_assign, name='shift_assign'),
    path('shifts/remove', views.shift_remove, name='shift_remove'),
    path('shifts/<int:pk>', views.shift_detail, name='shift_detail'),
    path('workforce/', views.user_list, name='user_list'),
    path('workforce/new', views.user_create, name='user_create'),
    path('workforce/<int:pk>', views.user_detail, name='user_detail'),
    path('export/', views.shift_export, name='shift_export'),
    path('dashboard/shifts', views.shift_visual, name='shift_visual'),
    path('dashboard/fillrate', views.fillrate_visual, name='fillrate_visual'),
]