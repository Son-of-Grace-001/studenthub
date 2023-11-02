from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path ('', views.home, name='home'),
  path ('login', views.login, name='login'),
  path ('signup', views.signup, name='signup'),
  path ('confirmation', views.sends, name='sending'),
  path ('dashboard', views.dashboard, name='dashboard'),
  path ('logout', views.logout, name='logout'),
  path ('department/<int:id>', views.department, name='department'),
  path ('courses/<int:id>', views.courses, name='courses'),
  path('level/<int:id>/', views.level, name='level'),
  path('material/<int:id>/', views.material, name='material'),
  path('year/<int:id>/', views.year, name='year'),
  path('reset_password/', auth_views.PasswordResetView.as_view(template_name='html/password_reset.html'), 
       name='reset_password'),
  path('reset_password_set/', auth_views.PasswordResetDoneView.as_view(template_name='html/resent.html'), 
       name='password_reset_done'),
  path('reset <uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='html/enterpassword.html'), 
       name='password_reset_confirm'),
  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='html/reset_done.html'), 
       name='password_reset_complete'),
  path ('activate/<uidb64>/<token>', views.activate, name='activate'),
]