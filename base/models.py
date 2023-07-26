from django.db import models

class MyModel(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True,null=True)

    class Meta:
        abstract = True