from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import redirect
from . import views


router = DefaultRouter()
router.register(r'cars', views.CarViewSet, basename='car')

def add_car_guest_redirect(request):
    messages.error(request, 'Только авторизованные пользователи могут добавлять автомобили.')
    return redirect('/')


urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('api/', include(router.urls)),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('add_car/', views.add_car, name='add_car'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('api/cars/<int:car_id>/comments/', views.car_comments, name='car_comments'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
