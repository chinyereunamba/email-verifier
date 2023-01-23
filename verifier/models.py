from django.db import models

# Create your models here.

class EmailList(models.Model):
    email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.email