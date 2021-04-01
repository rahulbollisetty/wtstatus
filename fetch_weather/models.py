from django.db import models
from django.conf import settings
class City(models.Model):
    name = models.CharField(max_length=25)
    uname= models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL)
    def _str_(self): #show the actual city name on the dashboard
        return self.name

    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'