from django.conf import settings
from django.db import models
from django.utils import timezone

class Jugdments(models.Model):
    title = models.TextField()
    orgao = models.TextField(default="Superior Tribunal de Justiça")
    processo = models.TextField(default="--")
    ementa = models.TextField(default= "ementa")
    texto = models.TextField(default="something's wrong")
    label_1 = models.TextField(default="IRPJ")
    label_2 = models.TextField(default="Lucro Real")
    label_3 = models.TextField(default="Rendimento interno")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Keyword(models.Model):
    keyword = models.TextField()
    judgment = models.ForeignKey(Jugdments, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

class UploadPdf(models.Model):
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)