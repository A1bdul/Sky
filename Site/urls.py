from django.contrib.auth.decorators import login_required
from django.urls import path
from Site import views
from django.conf import settings, urls
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('ajax-save-photo', views.ajaxsavephoto),
    path('ajax-photo-feed', views.ajaxphotofeed),
]
