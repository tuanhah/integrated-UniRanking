from django.db import models
from django.urls import reverse
from criteria.models import Score, ScoreByCategory


class University(models.Model):
    code = models.CharField(max_length=7, null=True)
    name = models.CharField(max_length=100)
    site_url = models.URLField(blank=True, null=True)
    image_path = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('University',on_delete=models.SET_NULL,blank=True, null=True)
    subjects = models.ManyToManyField('subject.Subject', through='UniversitySubject')
    ranking_position = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('university_info', kwargs={'id': self.pk})

    class Meta:
        db_table = "university"
        ordering = ['id']

class UniversityScoreByCategory(ScoreByCategory):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="scores_by_category")

    def __str__(self):
        score = str(self.score)
        return "{} | Category: {} | Score: {}".format(self.university, self.category_criterion, score)
        
    class Meta: 
        db_table = "university_score_by_category"
        ordering = ['id']

class UniversityScore(Score):
    score_by_category = models.ForeignKey(UniversityScoreByCategory,on_delete=models.CASCADE, blank=True, null=True, related_name="cri_scores") 

    def update_u_score_by_category(self):
        cri_data = self.score_by_category.cri_scores.all()
        cri_amount = cri_data.count()
        total_score = 0
        for cri in cri_data: 
            total_score += cri.score
        category_cri = self.score_by_category
        category_cri.score = total_score / cri_amount
        category_cri.save(update_fields=['score'])

    def save(self, university = None, *args, **kwargs):
        """
            Save UniversityScore record and update/create UniversityScoreByCategory
        """

        if university is not None:
            self_category = self.criterion.category
            self.score_by_category, created = university.scores_by_category.get_or_create(category_criterion = self_category)
        if self.score_by_category is not None:
            super().save(*args, **kwargs)
            self.update_u_score_by_category()

    def _university(self):
        return self.score_by_category.university

    class Meta:
        db_table = "university_score"
        ordering = ['id']

class UniversitySubject(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE, related_name="subject_set")
    subject = models.ForeignKey('subject.Subject',on_delete=models.CASCADE, related_name="universities")

    def subject_group(self):
        return self.subject.group
    def subject_name(self):
        return self.subject

    def __str__(self):
        return "University: {} | Subject: {}".format(self.university.name, self.subject.name)

    class Meta:
        db_table = "university_subject"
        ordering = ['id']

