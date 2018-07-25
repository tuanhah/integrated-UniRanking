from django.db import models

from university.models.base import University
from criterion.models import Criterion
from score.models import ScoreByCriterion, ScoreByCriterionCategory

class UniversityScoreByCriterionCategory(ScoreByCriterionCategory):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='criterion_category_scores')

    class Meta: 
        db_table = 'university_score_by_category'
        ordering = ['id']
        unique_together = ('university', 'criterion_category')

    def __str__(self):
        score = str(self.score)
        return '{} | Category: {} | Score: {}'.format(self.university, self.criterion_category, score)
    
    def update_university_avg_score_and_rank(self):
        self.university.update_avg_score_and_rank()

    def get_score_owner_object(self):
        return self.university
    

class UniversityScoreByCriterion(ScoreByCriterion):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='criterion_scores')
    
    class Meta:
        db_table = 'university_score'
        ordering = ['id']
        unique_together = ('university', 'criterion')

    def __str__(self):
        score = str(self.score)
        return '{} | Criterion: {} | Score: {}'.format(self.university, self.criterion, score)

    def get_score_owner_object(self):
        return self.university

    @property
    def is_editable(self):
        if not hasattr(self, "editable"):
            self.editable = self.get_editable_criterion_queryset().filter(id = self.criterion_id).exists()
        return self.editable

    @classmethod
    def get_editable_criterion_queryset(self):
        queryset = Criterion.objects.all()
        return queryset

