"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include


from firstapp.views import main,modify2, detail, credit, main_map, signup, login, new, create, search, post, profile, modify, edit, update, delete



import firstapp.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('main/', main, name='main'),
    path('detail/<str:id>', detail, name='detail'),
    path('create/', create, name='create'),
    path('credit/', credit, name='credit'),     
    path('map/', main_map, name='main_map'),
    path('', login, name='main_login'),
    path('accounts/', include('accounts.urls')),
    path('post/', post, name='post'),
    path('search/', search, name='search'),
    path('profile/<str:name>', profile, name='profile'),
    path('modify/<str:name2>', modify, name='modify'),
    path('modify2/', modify2, name="modify2"),
    path('edit/<str:id>', edit, name='edit'),
    path('update/<str:id>', update, name='update'),
    path('delete/<str:id>', delete, name='delete'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)