from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import University, UniversityScoreByCriterionCategory, UniversityScoreByCriterion, UserManagerUniversity

@receiver([post_save,], sender = University)
def create_university_profile(sender, instance, created, **kwargs):
    if created:
        instance.create_university_profile_object()

@receiver([post_save, post_delete], sender = UniversityScoreByCriterionCategory)
def update_score_and_rank(sender, instance, **kwargs):
    instance.update_university_avg_score_and_rank()

@receiver([post_save, post_delete], sender = UniversityScoreByCriterion)
def update_score_by_category(sender, instance, **kwargs):
    instance.update_criterion_category_score()

@receiver([post_save,], sender = UserManagerUniversity)
def add_manage_university_permission(sender, instance, **kwargs):
    instance.add_permissions()

@receiver([pre_delete,], sender = UserManagerUniversity)
def remove_manage_university_permission(sender, instance, **kwargs):
    instance.remove_permissions()

