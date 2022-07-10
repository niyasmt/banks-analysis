from django.db import models


class Details(models.Model):

    document = models.FileField(upload_to='files')
    name = models.CharField(max_length=100)
    predicted_balance = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.name


