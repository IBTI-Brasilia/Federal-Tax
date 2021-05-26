from django.conf import settings
from django.db import models
from django.utils import timezone

class Jugdments(models.Model):
    title = models.TextField()
    orgao = models.TextField(default="Superior Tribunal de Justiça")
    processo = models.TextField(default="--")
    ementa = models.TextField(default= "ementa")
    texto = models.TextField(default="something's wrong")
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

class Label_1(models.Model):
    label_1 = models.TextField()
    judgment = models.ForeignKey(Jugdments, on_delete=models.CASCADE, default="IRPJ")

class Label_2(models.Model):
    label_2 = models.TextField()
    label_1 = models.ForeignKey(Label_1, on_delete=models.CASCADE, default="Lucro Real")

class Label_3(models.Model):
    label_3 = models.TextField()
    label_2 = models.ForeignKey(Label_2, on_delete=models.CASCADE, default="Rendimento interno")