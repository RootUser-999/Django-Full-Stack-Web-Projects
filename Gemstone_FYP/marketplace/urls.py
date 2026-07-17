from django.urls import path
from . import views
from .views import CreateListingView, UploadImagesView

app_name = "marketplace"

urlpatterns = [

    path("", views.marketplace, name="marketplace"),

    path(
        "create/",
        CreateListingView.as_view(),
        name="create_listing"
    ),

    path(
        "upload-images/",
        UploadImagesView.as_view(),
        name="upload_images"
    ),

]