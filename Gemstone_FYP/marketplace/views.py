from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.edit import FormView

from .models import Listing
from .forms import ListingForm, ImageVerificationForm


# Marketplace home page
def marketplace(request):
    return render(
        request,
        "marketplace/marketplace.html"
    )


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
class UploadImagesView(LoginRequiredMixin, FormView):

    template_name = "marketplace/upload_images.html"
    form_class = ImageVerificationForm


    def dispatch(self, request, *args, **kwargs):

        # Check Step 1 completed
        if "listing_data" not in request.session:

            messages.warning(
                request,
                "Please complete the listing details first."
            )

            return redirect(
                "marketplace:create_listing"
            )


        return super().dispatch(
            request,
            *args,
            **kwargs
        )


    def form_valid(self, form):

        # Single image upload
        image = self.request.FILES["image"]


        # AI verification will be added here:
        #
        # 1. Save image temporarily
        # 2. Call binary model
        # 3. If gemstone:
        #       Call gemstone classifier
        #       Create Listing
        #       Save ListingImage
        #
        # 4. If not gemstone:
        #       Show error


        messages.success(
            self.request,
            "Image uploaded successfully. AI verification coming next."
        )


        return redirect(
            "marketplace:marketplace"
        )


    def form_invalid(self, form):

        messages.error(
            self.request,
            "Please upload a valid gemstone image."
        )


        return super().form_invalid(form)