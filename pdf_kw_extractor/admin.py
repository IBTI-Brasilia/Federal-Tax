from django.contrib import admin


from django.contrib import admin
from .models import Jugdments
from .models import UploadPdf, Keyword

# Register your models here.
admin.site.register(Jugdments)
admin.site.register(Keyword)
admin.site.register(UploadPdf)