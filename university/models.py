from django.db import models
from django.urls import reverse
from criteria.models import Score, ScoreByCategory


class University(models.Model):
    code = models.CharField(max_length=7, null=True)
    name = models.CharField(max_length=100)
    site_url = models.URLField(blank=True, null=True)
    image_path = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('University',on_delete=models.SET_NULL,blank=True, null=True, related_name="child_universities")
    subjects = models.ManyToManyField('subject.Subject', through='UniversitySubject')
    ranking_position = models.IntegerField(default=-1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('university_info', kwargs={'id': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        parent_univ = self.parent

    class Meta:
        db_table = "university"
        ordering = ['id']

class UniversityScoreByCategory(ScoreByCategory):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="scores_by_category")

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                self.university.scores_by_category.get(category_criterion = self.category_criterion)
            except UniversityScoreByCategory.DoesNotExist:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        score = str(self.score)
        return "{} | Category: {} | Score: {}".format(self.university, self.category_criterion, score)
        
    class Meta: 
        db_table = "university_score_by_category"
        ordering = ['id']

class UniversityScore(Score):
    score_by_category = models.ForeignKey(UniversityScoreByCategory,on_delete=models.CASCADE, blank=True, null=True, related_name="cri_scores") 

    def _university(self):
        return self.score_by_category.university
    
    def save(self, *args, **kwargs):
        """
            Save UniversityScore record and update/create UniversityScoreByCategory
        """
        if self.pk is None: #for creating new object
            try:
                existed_univ_score = self.score_by_category.cri_scores.get(criterion = self.criterion)
            except UniversityScore.DoesNotExist:
                super().save(*args, **kwargs)
            else:
                existed_univ_score.score = self.score
                existed_univ_score.save(update_fields = ["score"])
        else: #for editing object
            super().save(*args, **kwargs)
        self.update_score_by_category()

    def delete(self):
        super().delete()
        print("deleted")
        self.update_score_by_category()
        
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

