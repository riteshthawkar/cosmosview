from django.db import models

# Create your models here.
class Body(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=300)
    page_url = models.CharField(max_length=500, default="")
    img_url = models.CharField(max_length=500, default="")
    content_url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.category = self.category.lower()
        return super(Body, self).save(*args, **kwargs)


class Model_3D(models.Model):
    name = models.CharField(max_length=200)
    model_url = models.CharField(max_length=500, default="")
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
