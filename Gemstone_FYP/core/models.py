from django.db import models

class imageUpload(models.Model):
    gem_image = models.ImageField(upload_to="gemstones/")

    def __str__(self):
        return self.gem_image.name