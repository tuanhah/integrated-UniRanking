from django.db import models
from django.utils.translation import gettext as _

# from criterion.querysets import CriterionCategoryQueryset, CriterionQueryset

class CriterionCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        db_table = 'criterion_category'
        ordering = ['id']
        verbose_name = _('Criterion Category')
        verbose_name_plural = _('Criterion Categories')        

    def __str__(self):
        return self.name

    def parse_all_criterion_infos(self, named = True):
        criteria = self.criteria.all()
        parsed_criteria = [criterion.parse_info(named = named) for criterion in criteria]
        return parsed_criteria

    def parse_info(self, named = True):
        if named:
            data = {"id" : self.id, "name" : self.name}
        else:
            data = {"id" : self.id}
        return data

class Criterion(models.Model):
    category = models.ForeignKey(CriterionCategory, on_delete=models.CASCADE, related_name='criteria', verbose_name=_('Category'))
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    
    class Meta:
        db_table = 'criterion'
        ordering = ['category', 'id']
        verbose_name = _('Criterion')
        verbose_name_plural = _('Criterions')        


    def __str__(self):
        return self.name

    def parse_info(self, named = True):
        if named: 
            data = { "id" : self.id, "name" : self.name, "description" : self.description}
        else: 
            data = { "id" : self.id}
        return data
