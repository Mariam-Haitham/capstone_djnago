
from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from care_book_api.views import (
    HomeView, HomeDetails, AddHome, Signup, MyTokenObtainPairView,
     UserInvite, AddChild, ChildUpdate)

urlpatterns = [

    path("admin/", admin.site.urls),

    path("homes/", HomeView.as_view(), name="home_list"),
    path("homes/<int:home_id>/", HomeDetails.as_view(), name="home_detial"),
    path("homes/add/", AddHome.as_view(), name = "home_add"),
    

    path("child/add/<int:home_id>/", AddChild.as_view(), name="child_add"),
    path("child/<int:child_id>/update/", ChildUpdate.as_view(), name="child_update"),

    path("signup/", Signup.as_view(), name="signup"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"), 
    path("invite/<int:home_id>/<str:type>/", UserInvite.as_view(), name="invite"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
