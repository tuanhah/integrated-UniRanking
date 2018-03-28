from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import SubjectScoreByCategory, SubjectScore

@receiver([post_save, post_delete], sender = SubjectScoreByCategory)
def update_overall_score(sender, instance, **kwargs):
    instance.update_overall_score()
    instance.update_rank()

@receiver([post_save, post_delete], sender = SubjectScore)
def update_score_by_category(sender, instance, **kwargs):
    instance.update_score_by_category()
    instance.update_u_score()

