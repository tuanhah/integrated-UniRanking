from django.db import models

from .base import UniversitySubject
from criterion.models import Criterion
from score.models import ScoreByCriterion, ScoreByCriterionCategory

# class SubjectScoreByCriterionCategory(ScoreByCriterionCategory):
#     univ_subject = models.ForeignKey(UniversitySubject, on_delete=models.CASCADE, related_name='criterion_category_scores')

#     class Meta: 
#         db_table = 'subject_score_by_category'
#         ordering = ['id']
#         unique_together = ('univ_subject', 'criterion_category')
    
#     def __str__(self):
#         score = str(self.score)
#         return 'University: {} | Subject: {} | Category: {} | Score: {}'.format(self.university(), self.subject(), self.criterion_category, score)

#     def update_univ_subject_avg_score_and_rank(self):
#         self.univ_subject.update_avg_score_and_rank()

#     def university(self):
#         return self.univ_subject.university
#     university.short_description= 'University'
    
#     def subject(self):
#         return self.univ_subject.subject
#     subject.short_description = 'Subject'

#     def get_score_owner_object(self):
#         return self.univ_subject

# class SubjectScoreByCriterion(ScoreByCriterion):
#     univ_subject = models.ForeignKey(UniversitySubject, on_delete=models.CASCADE, related_name='criterion_scores')

#     class Meta:
#         db_table = 'subject_score'
#         ordering = ['id']
#         unique_together = ('univ_subject', 'criterion')

#     def __str__(self):
#         score = str(self.score)
#         return 'University: {} | Subject: {} | Criterion: {} | Score: {}'.format(self.university(), self.subject(), self.criterion, score)

#     def update_university_criterion_score(self):
#         university = self.university()
#         university_criterion_score, created = university.criterion_scores.get_or_create(criterion_id = self.criterion_id)
#         university_criterion_score.update_score()

#     def get_score_owner_object(self):
#         return self.univ_subject

#     @classmethod
#     def get_editable_criterion_queryset(cls):
#         queryset = Criterion.objects.subject_only()
#         return queryset
        
#     def university(self):
#         return self.univ_subject.university
#     university.short_description= "University"
    
#     def subject(self):
#         return self.univ_subject.subject
#     subject.short_description = "Subject"