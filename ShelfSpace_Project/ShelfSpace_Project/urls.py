"""
URL configuration for ShelfSpace_Project project.

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
from django.urls import path, include
from accounts import views as acviews

urlpatterns = [
    path('', acviews.homepage, name='home'),
    path('login/', acviews.login, name='login'),
    path('signup/', acviews.signup, name='signup'),
    path('logout/', acviews.logout, name='logout'),
    path('books/', include('books.urls')),
    path('QuotesSharing/', include('ShelfSpaceBlogs.urls')),
    path('admin/', admin.site.urls),
]
