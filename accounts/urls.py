from .views import HomeView, LogoutView, PasswordResetView, RegistComplete, user_login, user_regist
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    # path('home/', HomeView.as_view(), name='home'),
    path('regist/', user_regist, name='regist'),
    path('password_reset/<uuid:token>', PasswordResetView.as_view(), name='password_reset'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('complete/', RegistComplete.as_view(), name='regist_complete'),
]
