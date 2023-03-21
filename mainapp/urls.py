from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('add_user', views.add_user, name='add_user'),
    path('update_user/<int:pk>', views.update_user, name='update_user'),
    path('delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('user/<int:pk>', views.user_page, name='user_page'),
    path('users', views.accepted_user, name='users'),
    path('today', views.today, name='today'),
    path('full', views.full, name='full'),
]
