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

MODEL_PATH = os.path.join(settings.BASE_DIR, "model", "best_model.keras")
model = tf.keras.models.load_model(MODEL_PATH)

class_names = [
    "Alexandrite", "Amber", "Cats Eye", "Malachite", "Morganite",
    "aquamarine", "diamond", "emerald", "fluorite green",
    "fluorite purple", "garnet", "peridot", "ruby",
    "sapphire blue", "sapphire pink", "topaz blue",
    "topaz yellow", "tourmaline black", "turquoise", "zircon"
]

@csrf_exempt
@api_view(["POST"])
def predict_gemstone(request):
    try:
        image_file = request.FILES["image"]

        # Open image
        # image = Image.open(image_file).convert("RGB")
        # image = image.resize((224, 224))
        from PIL import ImageOps

        image = Image.open(image_file)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = image.resize((224, 224))

        # Convert to array
        # img_array = np.array(image) / 255.0
        # img_array = np.expand_dims(img_array, axis=0)
        img_array = np.array(image).astype("float32")
        img_array = np.expand_dims(img_array, axis=0)

        img_array = tf.keras.applications.efficientnet_v2.preprocess_input(
            img_array
        )

        # Prediction
        predictions = model.predict(img_array)
        class_index = np.argmax(predictions)
        confidence = float(np.max(predictions))

        result = {
            "class": class_names[class_index],
            "confidence": confidence
        }

        return Response(result)

    except Exception as e:
        return Response({"error": str(e)})

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

# class PredictView(CreateView):
#     model = imageUpload
#     form_class = ImageUploadForm
#     template_name = "core/result.html"

#     def form_valid(self, form):
#         # Save uploaded image
#         self.object = form.save()

#         # Predict gemstone
#         prediction, confidence, all_predictions = predict(
#             self.object.gem_image.path
#         )

#         # Always render the result page
#         return render(
#             self.request,
#             "core/result.html",
#             {
#                 "form": ImageUploadForm(),
#                 "image": self.object,
#                 "prediction": prediction,
#                 "confidence": round(confidence, 2),
#                 "all_predictions": all_predictions,
#             },
#         )

class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"



def marketplace(request):
    return render(request, "core/marketplace.html")


def messages(request):
    return render(request, "core/messages.html")