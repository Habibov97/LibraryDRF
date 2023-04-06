from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Kitab(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    yayim_tarixi = models.DateTimeField()
    yaradilma_tarixi = models.DateTimeField(auto_now_add=True)
    yenilenme_tarixi = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.isim} - {self.yazar}'    
    

class Yorum(models.Model):
    kitab = models.ForeignKey(Kitab, on_delete=models.CASCADE, related_name='yorumlar')
    yorum_sahibi = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kullanici_yorumlari')
    yorum = models.TextField(blank=True, null=True)
    yaradilma_tarixi = models.DateTimeField(auto_now_add=True)
    yenilenme_tarixi = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],)

    def __str__(self):
        return str(self.rating)

