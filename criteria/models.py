from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class CriterionCategory(models.Model):
    name = models.CharField(max_length=50)
    university_only = models.BooleanField(default = False) #indenfy whether this category criterion is represented on university level only (not particular subject)
    
    class Meta:
        db_table = 'criterion_category'
        ordering = ['id']

    def __str__(self):
        return self.name

class Criterion(models.Model):
    category = models.ForeignKey(CriterionCategory, on_delete=models.CASCADE, related_name='criteria')
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'criterion'
        ordering = ['id']

    def __str__(self):
        return self.name

class ScoreByCategory(models.Model):
    criterion_category = models.ForeignKey(CriterionCategory, on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.score)

class Score(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    score_by_category = 'A foreign key to a score by category table, will be defined in the child class'

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.score)

    def update_score_by_category(self):
        try:
            cri_category_score = self.score_by_category
        except ObjectDoesNotExist:
            #handled when this record is deleted before post delete is triggered (ex:  on cascade delete category_criterion)
            pass 
        else:
            avg_score = cri_category_score.cri_scores.aggregate(models.Avg('score'))
            avg_score = avg_score.get('score__avg')
            if avg_score is not None:
                cri_category_score.score = round(avg_score, 2)
                cri_category_score.save(update_fields = ['score'])
            else:
                cri_category_score.delete()
