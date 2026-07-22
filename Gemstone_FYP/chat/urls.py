from django.urls import path

from .views import (
    ConversationListView,
    ConversationDetailView,
    StartConversationView,
)

app_name = "chat"

urlpatterns = [

    path(
        "",
        ConversationListView.as_view(),
        name="conversation_list",
    ),

    path(
        "start/<int:listing_id>/",
        StartConversationView.as_view(),
        name="start_conversation",
    ),

    path(
        "conversation/<int:pk>/",
        ConversationDetailView.as_view(),
        name="conversation_detail",
    ),
]