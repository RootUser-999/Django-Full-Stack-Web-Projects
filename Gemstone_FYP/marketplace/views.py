from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormView
from .models import Listing, ListingImage
from .forms import ListingForm, ImageVerificationForm
from django.db.models import Q
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from core import predictor

# Marketplace home page


from django.db.models import Q
from django.shortcuts import render


def marketplace(request):

    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()

    listings = (
        Listing.objects
        .filter(is_ai_verified=True)
        .select_related("seller")
        .prefetch_related("images")
    )

    # ================= Search =================

    if search:

        listings = listings.filter(

            Q(title__icontains=search) |
            Q(ai_prediction__icontains=search) |
            Q(description__icontains=search) |
            Q(origin__icontains=search) |
            Q(seller__username__icontains=search)

        )

    # ================= Category Filter =================

    if category:
        listings = listings.filter(
            ai_prediction__icontains=category.strip()
        )

    listings = listings.order_by("-created_at")

    context = {

        "listings": listings,
        "search": search,
        "category": category,

    }

    return render(

        request,
        "marketplace/marketplace.html",
        context,

    )

class ListingDetailView(DetailView):

    model = Listing

    template_name = "marketplace/listing_detail.html"

    context_object_name = "listing"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # All images of this listing
        context["images"] = self.object.images.all()

        # Related gemstones (same type)
        context["related_listings"] = (
            Listing.objects.filter(
                ai_prediction=self.object.ai_prediction,
                status="Available"
            )
            .exclude(pk=self.object.pk)[:4]
        )

        return context


# Step 1: Create Listing Details
class CreateListingView(LoginRequiredMixin, CreateView):

    model = Listing
    form_class = ListingForm
    template_name = "marketplace/create_listing.html"


    def form_valid(self, form):

        # Convert Decimal values before saving into session
        listing_data = {}

        for key, value in form.cleaned_data.items():

            if isinstance(value, Decimal):
                listing_data[key] = str(value)

            else:
                listing_data[key] = value


        # Store details temporarily
        self.request.session["listing_data"] = listing_data


        messages.info(
            self.request,
            "Details saved. Now upload gemstone images for AI verification."
        )


        return redirect(
            "marketplace:upload_images"
        )


    def form_invalid(self, form):

        messages.error(
            self.request,
            "Please correct the errors below."
        )

        return super().form_invalid(form)



# Step 2: Upload Images
# class UploadImagesView(LoginRequiredMixin, FormView):

#     template_name = "marketplace/upload_images.html"
#     form_class = ImageVerificationForm

#     def dispatch(self, request, *args, **kwargs):

#         if "listing_data" not in request.session:

#             messages.warning(
#                 request,
#                 "Please complete the listing details first."
#             )

#             return redirect("marketplace:create_listing")

#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):

#         uploaded_image = self.request.FILES["image"]

#         # Save uploaded image temporarily
#         temp_path = default_storage.save(
#             f"temp/{uploaded_image.name}",
#             ContentFile(uploaded_image.read())
#         )

#         image_path = default_storage.path(temp_path)

#         try:

#             # Run AI prediction
#             predicted_class, confidence, all_predictions = predictor.predict(image_path)

#             # --------------------------------------------------
#             # Image is NOT a gemstone
#             # --------------------------------------------------
#             if predicted_class is None:

#                 messages.error(
#                     self.request,
#                     "The uploaded image is not recognized as a gemstone. Please upload a valid gemstone image."
#                 )

#                 return redirect("marketplace:upload_images")

#             # --------------------------------------------------
#             # Image IS a gemstone
#             # --------------------------------------------------

#             listing_data = self.request.session.get("listing_data")

#             listing = Listing.objects.create(

#                 seller=self.request.user,

#                 title=listing_data["title"],
#                 description=listing_data["description"],

#                 price=Decimal(listing_data["price"]),
#                 weight=Decimal(listing_data["weight"]),

#                 color=listing_data["color"],
#                 origin=listing_data["origin"],
#                 shape=listing_data["shape"],
#                 dimensions=listing_data["dimensions"],
#                 treatment=listing_data["treatment"],
#                 certification=listing_data["certification"],

#                 quantity=listing_data["quantity"],
#                 condition=listing_data["condition"],
#                 status=listing_data["status"],

#                 gemstone_type=predicted_class,

#                 ai_prediction=predicted_class,
#                 ai_confidence=confidence,
#                 is_ai_verified=True,
#             )

#             # Save original uploaded image
#             uploaded_image.seek(0)

#             ListingImage.objects.create(

#                 listing=listing,
#                 image=uploaded_image,

#             )

#             # Remove session data
#             del self.request.session["listing_data"]
#             print("Listing Saved Successfully")
#             print(predicted_class)
#             print(confidence)
#             messages.success(

#                 self.request,
#                 f"Listing published successfully! "
#                 f"AI identified your gemstone as "
#                 f"{predicted_class} "
#                 f"with {confidence:.2f}% confidence."
#             )

#             return redirect("marketplace:marketplace")

#         finally:

#             # Delete temporary image
#             if default_storage.exists(temp_path):
#                 default_storage.delete(temp_path)

#     def form_invalid(self, form):

#         messages.error(
#             self.request,
#             "Please upload a valid image."
#         )

#         return super().form_invalid(form)
class UploadImagesView(LoginRequiredMixin, FormView):

    template_name = "marketplace/upload_images.html"
    form_class = ImageVerificationForm

    def dispatch(self, request, *args, **kwargs):

        if "listing_data" not in request.session:

            messages.warning(
                request,
                "Please complete the listing details first."
            )

            return redirect("marketplace:create_listing")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        uploaded_image = self.request.FILES["image"]

        listing_data = self.request.session.get("listing_data")

        listing = Listing.objects.create(

            seller=self.request.user,

            title=listing_data["title"],
            description=listing_data["description"],

            price=Decimal(listing_data["price"]),
            weight=Decimal(listing_data["weight"]),

            color=listing_data["color"],
            origin=listing_data["origin"],
            shape=listing_data["shape"],
            dimensions=listing_data["dimensions"],
            treatment=listing_data["treatment"],
            certification=listing_data["certification"],

            quantity=listing_data["quantity"],
            condition=listing_data["condition"],
            status=listing_data["status"],

            # Temporary values until AI is enabled again
            gemstone_type="Not Verified",
            ai_prediction="Pending Verification",
            ai_confidence=0.0,
            is_ai_verified=True,
        )

        ListingImage.objects.create(

            listing=listing,
            image=uploaded_image,

        )

        del self.request.session["listing_data"]

        messages.success(

            self.request,
            "Listing published successfully."

        )

        return redirect("marketplace:marketplace")

    def form_invalid(self, form):

        messages.error(

            self.request,
            "Please upload a valid image."

        )

        return super().form_invalid(form)