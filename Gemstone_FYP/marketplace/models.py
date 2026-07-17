from django.db import models
from django.conf import settings


class Listing(models.Model):

    GEMSTONE_CHOICES = [
        ("Alexandrite", "Alexandrite"),
        ("Amber", "Amber"),
        ("Cats Eye", "Cats Eye"),
        ("Malachite", "Malachite"),
        ("Morganite", "Morganite"),
        ("Aquamarine", "Aquamarine"),
        ("Diamond", "Diamond"),
        ("Emerald", "Emerald"),
        ("Fluorite Green", "Fluorite Green"),
        ("Fluorite Purple", "Fluorite Purple"),
        ("Garnet", "Garnet"),
        ("Peridot", "Peridot"),
        ("Ruby", "Ruby"),
        ("Sapphire Blue", "Sapphire Blue"),
        ("Sapphire Pink", "Sapphire Pink"),
        ("Topaz Blue", "Topaz Blue"),
        ("Topaz Yellow", "Topaz Yellow"),
        ("Tourmaline Black", "Tourmaline Black"),
        ("Turquoise", "Turquoise"),
        ("Zircon", "Zircon"),
    ]

    CONDITION_CHOICES = [
        ("Rough", "Rough"),
        ("Cut", "Cut"),
        ("Polished", "Polished"),
        ("Faceted", "Faceted"),
        ("Cabochon", "Cabochon"),
    ]

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Reserved", "Reserved"),
        ("Sold", "Sold"),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    title = models.CharField(max_length=200)

    gemstone_type = models.CharField(
        max_length=50,
        choices=GEMSTONE_CHOICES,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    color = models.CharField(max_length=100)

    origin = models.CharField(max_length=100)

    shape = models.CharField(max_length=100)

    dimensions = models.CharField(
        max_length=100,
        blank=True
    )

    treatment = models.CharField(
        max_length=100,
        blank=True
    )

    certification = models.CharField(
        max_length=100,
        blank=True
    )

    quantity = models.PositiveIntegerField(default=1)

    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    ai_prediction = models.CharField(
        max_length=100,
        blank=True
    )

    ai_confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_ai_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ListingImage(models.Model):

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="marketplace/listings/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.listing.title} Image"