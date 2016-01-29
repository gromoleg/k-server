from __future__ import unicode_literals

from django.db import models
from response.templates import ok_response


class Faculty(models.Model):
    name = models.CharField(blank=True, default='', max_length=300)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all():
        res = [{'id': _faculty.id, 'name': _faculty.name} for _faculty in Faculty.objects.all()]
        return ok_response(res)