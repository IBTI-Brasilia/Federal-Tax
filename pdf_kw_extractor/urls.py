from django.urls import path
from . import views
from pdf_kw_extractor.views import HomeView

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('list_keywords', views.list_keywords, name='list_keywords'),
    path('view_more/<id>', views.view_more),
    path('submit', views.submit_login, name='submit_login'),
    path("logout", views.logout_request, name="logout"),
    path('view_more/delete/<id>', views.delete_process),
    path('view_more/download_pdf/<id>', views.download_pdf, name='download_pdf'),
    path('home/', HomeView.as_view()),
]