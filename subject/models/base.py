from django.db import models, connection

from score.models import ScoreByCriterionCategory, ScoreByCriterion
from score.querysets import ScoreOwnerQueryset
from university.models import University
from score.mixins import ScoreOwnerMixin, ScoreParserMixin
from subject.querysets import SubjectGroupQueryset

from django.utils.translation import gettext as _


class Sector(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    universities = models.ManyToManyField('university.University', through='subject.UniversitySector', related_name='sector_set')


    class Meta:
        db_table = 'sector'
        ordering = ['id']
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')        


    def __str__(self):
        return self.name

    def parse_profile(self):
        data = {"id" : self.id, "name" : self.name}
        return data

class UniversitySector(models.Model, ScoreOwnerMixin, ScoreParserMixin):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='sectors_set', verbose_name=_('University'))
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='universities_set', verbose_name=_('Sector'))
    
    class Meta:
        db_table = 'university_sector'
        ordering = ['id']
        unique_together = ('university', 'sector')
        verbose_name = _('University Sector')
        verbose_name_plural = _('Universities Sectors')        

    def __str__(self):
        return "University: {} | Subject: {}".format(self.university.name, self.sector.name)