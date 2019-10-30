
from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from care_book_api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.MyTokenObtainPairView.as_view(), name='login'), 
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
