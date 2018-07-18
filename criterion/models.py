from django.db import models

# from criterion.querysets import CriterionCategoryQueryset, CriterionQueryset

class CriterionCategory(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'criterion_category'
        ordering = ['id']

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
    category = models.ForeignKey(CriterionCategory, on_delete=models.CASCADE, related_name='criteria')
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    
    class Meta:
        db_table = 'criterion'
        ordering = ['category', 'id']

    def __str__(self):
        return self.name

    def parse_info(self, named = True):
        if named: 
            data = { "id" : self.id, "name" : self.name, "description" : self.description}
        else: 
            data = { "id" : self.id}
        return data
