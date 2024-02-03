"""
URL configuration for redmine_mass_editor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from mass_editor.views import step_one, step_two, step_three, download_data, upload_data, step_four, step_five, progress, stop_process
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy



urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('step_one')), name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('step-one/', step_one, name='step_one'),
    path('step-two/', step_two, name='step_two'),
    path('step-three/', step_three, name='step_three'),
    path('download-data/', download_data, name='download_data'),
    path('upload-data/', upload_data, name='upload_data'),
    path('step-four/', step_four, name='step_four'),
    path('step-five/', step_five, name='step_five'),
    path('progress/', progress, name='progress'),
    path('stop-process/', stop_process, name='stop_process'),
]
