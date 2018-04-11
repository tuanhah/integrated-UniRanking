from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import SubjectScoreByCriterionCategory, SubjectScoreByCriterion

@receiver([post_save, post_delete], sender = SubjectScoreByCriterionCategory)
def update_score_and_rank(sender, instance, **kwargs):
    instance.update_univ_subject_avg_score_and_rank()

@receiver([post_save, post_delete], sender = SubjectScoreByCriterion)
def update_score_by_category(sender, instance, **kwargs):
    instance.update_criterion_category_score()
    instance.update_university_criterion_score()

