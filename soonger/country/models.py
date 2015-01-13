from django.db import models


class Country(models.Model):
    keycountry = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=50, verbose_name='nombre')

    class Meta:
        db_table = 'countries'
        verbose_name = 'country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name