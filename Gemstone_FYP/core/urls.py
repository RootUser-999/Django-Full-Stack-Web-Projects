from . import views
from django.urls import path

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("upload/", views.PredictView.as_view(), name="image_upload"),
    path("predict/", views.predict_gemstone),
    path("marketplace/", views.marketplace, name="marketplace"),
    path("messages/", views.messages, name="messages"),
    
]
