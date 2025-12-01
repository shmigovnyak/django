from django.urls import path
from . import views
app_name = "news"
urlpatterns = [
    path('', views.index_start, name='index_start'),
    path('news/', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path("detail/<int:pk>/", views.detail, name='news_detail'),
    path("create/", views.create_news, name='create_news'),
    path("update/<int:pk>/", views.update_news, name='update_news'),
]