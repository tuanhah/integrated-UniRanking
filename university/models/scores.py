from django.db import models

from university.models.base import University
from criterion.models import Criterion
from score.models import ScoreByCriterion, ScoreByCriterionCategory
from django.utils.translation import gettext as _

class UniversityScoreByCriterionCategory(ScoreByCriterionCategory):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='criterion_category_scores', verbose_name=_('University'))

    class Meta: 
        db_table = 'university_score_by_category'
        ordering = ['id']
        unique_together = ('university', 'criterion_category')
        verbose_name = _('University Score By Criterion Category')   
        verbose_name_plural = _('University Scores By Criterion Categories')   
        

    def __str__(self):
        score = str(self.score)
        return _('{} | Category: {} | Score: {}'.format(self.university, self.criterion_category, score))
    
    def update_university_avg_score_and_rank(self):
        self.university.update_avg_score_and_rank()

    def get_score_owner_object(self):
        return self.university
    

class UniversityScoreByCriterion(ScoreByCriterion):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='criterion_scores', verbose_name=_('University'))
    
    class Meta:
        db_table = 'university_score'
        ordering = ['id']
        unique_together = ('university', 'criterion')
        verbose_name = _('University Score By Criterion')   
        verbose_name_plural = _('University Scores By Criterions')   
        

    def __str__(self):
        score = str(self.score)
        return _('{} | Criterion: {} | Score: {}'.format(self.university, self.criterion, score))

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

