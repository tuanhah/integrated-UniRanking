from django.db import models, connection
from django.urls import reverse

from criteria.models import Score, ScoreByCategory


class University(models.Model):
    code = models.CharField(max_length=7, null=True)
    name = models.CharField(max_length=100)
    overview = models.TextField(blank = True, null=True)
    site_url = models.URLField(blank=True, null=True)
    image_path = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('University', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_universities')
    subjects = models.ManyToManyField('subject.Subject', through='UniversitySubject')
    overall_score = models.FloatField(default=0)
    rank = models.IntegerField(default=-1)

    class Meta:
        db_table = 'university'
        ordering = ['id']   

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('university_profile', kwargs={'id': self.pk})

class UniversityScoreByCategory(ScoreByCategory):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='scores_by_category')

    class Meta: 
        db_table = 'university_score_by_category'
        ordering = ['id']
        unique_together = ('university', 'criterion_category')

    def __str__(self):
        score = str(self.score)
        return '{} | Category: {} | Score: {}'.format(self.university, self.criterion_category, score)
    
    def update_overall_score(self):
        self_model = self.__class__
        avg_score = self_model.objects.filter(university = self.university_id).aggregate(models.Avg('score'))
        avg_score = avg_score['score__avg'] or 0
        University.objects.filter(id = self.university_id).update(overall_score = round(avg_score, 2), rank = -1)
        
    def update_rank(self):
        university_table_name = University._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute('SET @rank = 0')
            cursor.execute('UPDATE {} SET rank = @rank:=(@rank + 1) WHERE overall_score > 0 ORDER BY overall_score DESC'.format(
                university_table_name)
            )


class UniversityScore(Score):
    score_by_category = models.ForeignKey(UniversityScoreByCategory, on_delete=models.CASCADE, related_name='cri_scores') 
    
    class Meta:
        db_table = 'university_score'
        ordering = ['id']
        unique_together = ('score_by_category', 'criterion')
    
    def _university(self):
        return self.score_by_category.university

class UniversitySubject(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='subject_set')
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE, related_name='universities')
    overall_score = models.FloatField(default=0, blank=True)
    rank = models.IntegerField(default=-1, blank=True)

    class Meta:
        db_table = 'university_subject'
        ordering = ['id']
        unique_together = ('university', 'subject')
    
    def __str__(self):
        return "University: {} | Subject: {}".format(self.university.name, self.subject.name)

    def get_absolute_url(self):
        return reverse('university_profile', kwargs={'id': self.id})
        
    def subject_group(self):
        return self.subject.group

    def subject_name(self):
        return self.subject

