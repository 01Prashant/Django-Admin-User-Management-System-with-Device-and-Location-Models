from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', LoginView.as_view(), name='login'),
    path('forgot/', ForgotView.as_view(), name='forgot'),
    path('otp/', OTPView.as_view(), name='otp'),
    path('reset/', ResetView.as_view(), name='reset'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('display/', DisplayView.as_view(), name='display'),
    path('addDevice/<int:id>/', AddDeviceView.as_view(), name='addDevice'),
    path('editDevice/<int:id>/', EditDeviceView.as_view(), name='editDevice'),
    path('deleteDevice/<int:id>/', DeleteDeviceView.as_view(), name='deleteDevice'),
    path('editUser/<int:id>/', EditUserView.as_view(), name='editUser'),
    path('addUser/<int:id>/', AddUserView.as_view(), name='addUser'),
    # path('deleteUser/<int:id>/', DeleteUserView.as_view(), name='deleteUser'),
]