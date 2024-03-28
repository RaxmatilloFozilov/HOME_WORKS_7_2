from django.urls import path
from .views import register, login_view, logout_view
from . import views

urlpatterns = [
    path('login/', register, name='login'),
    path('logout/', register, name='logout'),
    path('register/', register, name='register'),
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
    path('edit_news/<int:news_id>/', views.edit_news, name='edit_news'),
    path('add_news/', views.add_news, name='add_news'),

]
