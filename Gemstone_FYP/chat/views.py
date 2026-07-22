from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from marketplace.models import Listing
from .models import Conversation
from django.db.models import Q
from django.views.generic import ListView

class StartConversationView(LoginRequiredMixin, View):

    def get(self, request, listing_id):

        # Get the listing
        listing = get_object_or_404(
            Listing,
            pk=listing_id
        )

        buyer = request.user
        seller = listing.seller

        # Prevent chatting with yourself
        if buyer == seller:
            return redirect(
                "marketplace:listing_detail",
                pk=listing.id,
            )

        # Find existing conversation or create a new one
        conversation, created = Conversation.objects.get_or_create(
            buyer=buyer,
            seller=seller,
            listing=listing,
        )

        # Redirect to the conversation page
        return redirect(
            "chat:conversation_detail",
            pk=conversation.pk,
        )


from .forms import MessageForm


class ConversationDetailView(LoginRequiredMixin, DetailView):

    model = Conversation
    template_name = "chat/conversation_detail.html"
    context_object_name = "conversation"

    def get_queryset(self):

        return Conversation.objects.filter(
            buyer=self.request.user
        ) | Conversation.objects.filter(
            seller=self.request.user
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        conversation = self.object

        # Mark unread messages as read
        conversation.messages.filter(
            is_read=False
        ).exclude(
            sender=self.request.user
        ).update(
            is_read=True
        )

        context["messages"] = (
            conversation.messages
            .select_related("sender")
            .order_by("created_at")
        )

        context["form"] = MessageForm()

        context["listing"] = conversation.listing

        if self.request.user == conversation.buyer:
            context["other_user"] = conversation.seller
        else:
            context["other_user"] = conversation.buyer

        return context

        
# class ConversationListView(LoginRequiredMixin, ListView):

#     model = Conversation

#     template_name = "chat/conversation_list.html"

#     context_object_name = "conversations"

#     def get_queryset(self):

#         return (
#             Conversation.objects
#             .filter(
#                 Q(buyer=self.request.user) |
#                 Q(seller=self.request.user)
#             )
#             .select_related(
#                 "buyer",
#                 "seller",
#                 "listing",
#             )
#             .order_by("-updated_at")
#         )
class ConversationListView(LoginRequiredMixin, ListView):

    model = Conversation
    template_name = "chat/conversation_list.html"
    context_object_name = "conversations"

    def get_queryset(self):

        return (
            Conversation.objects
            .filter(
                Q(buyer=self.request.user) |
                Q(seller=self.request.user)
            )
            .select_related(
                "buyer",
                "seller",
                "listing",
            )
            .order_by("-updated_at")
        )