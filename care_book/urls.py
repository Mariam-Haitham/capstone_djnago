
from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from care_book_api import views

urlpatterns = [

    path("admin/", admin.site.urls),

    path("homes/", views.HomeList.as_view(), name="home_list"),
    path("homes/<int:home_id>/", views.HomeView.as_view(), name="home"),

    path("add/child/<int:home_id>/", views.AddChild.as_view(), name="add_child"),
	path("children/<int:home_id>/", views.ChildList.as_view(), name="children"),
    path("children/<int:child_id>/", views.ChildDetails.as_view(), name="child"),
    path("child/<int:child_id>/update/", views.ChildUpdate.as_view(), name="update_child"),

    path("signup/", views.Signup.as_view(), name="signup"),
    path("login/", views.MyTokenObtainPairView.as_view(), name="login"), 
    path("invite/<int:home_id>/", views.UserInvite.as_view(), name="invite"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
