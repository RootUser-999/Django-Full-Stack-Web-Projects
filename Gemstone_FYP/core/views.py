import os

from django.shortcuts import render
from .forms import ImageUploadForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, CreateView
from .models import imageUpload
from django.conf import settings

from .predictor import predict
# Create your views here.
from django.views.generic import TemplateView

import numpy as np
import tensorflow as tf
from PIL import Image
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# MODEL_PATH = os.path.join(settings.BASE_DIR, "model", "best_model.keras")
# model = tf.keras.models.load_model(MODEL_PATH)

@csrf_exempt
@api_view(["POST"])
def predict_gemstone(request):
    try:
        if "image" not in request.FILES:
            return Response(
                {"error": "No image file uploaded."},
                status=400
            )

        image_file = request.FILES["image"]

        # Save uploaded image temporarily
        temp_path = default_storage.save(
            f"temp/{image_file.name}",
            ContentFile(image_file.read())
        )

        image_path = default_storage.path(temp_path)

        try:
            predicted_class, confidence, all_predictions = predict(image_path)

            # Image is not a gemstone OR confidence too low
            # Image is not a gemstone
            if predicted_class is None:
                return Response({
                    "success": False,
                    "message": "The uploaded image is not a gemstone.",
                    "confidence": round(confidence, 2)
                })

            # Successful prediction
            return Response({
                "success": True,
                "class": predicted_class,
                "confidence": round(confidence, 2),
                "predictions": all_predictions
            })

        finally:
            # Delete temporary image
            if default_storage.exists(temp_path):
                default_storage.delete(temp_path)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=400
        )

@method_decorator(never_cache, name='dispatch')
class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ImageUploadForm()
        return context





from django.views.generic import CreateView

from django.shortcuts import render
from django.views.generic import CreateView
@method_decorator(never_cache, name='dispatch')
class PredictView(CreateView):
    model = imageUpload
    form_class = ImageUploadForm
    template_name = "core/result.html"

    def form_valid(self, form):
        # Save uploaded image
        self.object = form.save()

        # Predict gemstone
        prediction, confidence, all_predictions = predict(
            self.object.gem_image.path
        )

        # Reject invalid image
        if prediction is None:

            # Remove uploaded file
            if self.object.gem_image:
                self.object.gem_image.delete(save=False)

            # Remove database record
            self.object.delete()

            return render(
                self.request,
                "core/reject.html",
                {
                    "form": ImageUploadForm(),
                    "warning": "This image doesn't appear to be one of the supported gemstones. Please upload a clear image of a supported gemstone.",
                    "confidence": round(confidence, 2),
                },
            )

        # Valid prediction
        return render(
            self.request,
            "core/result.html",
            {
                "form": ImageUploadForm(),
                "image": self.object,
                "prediction": prediction,
                "confidence": round(confidence, 2),
                "all_predictions": all_predictions,
            },
        )



class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"



def marketplace(request):
    return render(request, "core/marketplace.html")


def messages(request):
    return render(request, "core/messages.html")