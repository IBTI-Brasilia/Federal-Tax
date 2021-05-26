from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('list_keywords', views.list_keywords, name='list_keywords'),
    path('view_more/<id>', views.view_more),
    path('submit', views.submit_login, name='submit_login'),
    path("logout", views.logout_request, name="logout"),
]