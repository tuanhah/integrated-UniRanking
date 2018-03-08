from django.db import models
from criteria.models import Score, ScoreByCategory

class GroupSubject(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('GroupSubject', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "group_subject"
        ordering = ['id']

    def __str__(self):
        return self.name

class Subject(models.Model):
    group = models.ForeignKey(GroupSubject,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def root_group(self):
        group = self.group
        return group if group.parent is None else group.parent

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "subject"
        ordering = ['id']


class SubjectScoreByCategory(ScoreByCategory):
    univ_subject = models.ForeignKey('university.UniversitySubject', on_delete=models.CASCADE, related_name="scores_by_category")

    def __str__(self):
        score = str(self.score)
        return "University: {} | Subject: {} | Category: {} | Score: {}".format(self._university(),self._subject(), self.category_criterion, score)

    def _university(self):
        return self.univ_subject.university
    _university.short_description= "University"
    
    def _subject(self):
        return self.univ_subject.subject
    _subject.short_description = "Subject"
    
    class Meta: 
        db_table = "subject_score_by_category"
        ordering = ['id']

class SubjectScore(Score):
    score_by_category = models.ForeignKey(SubjectScoreByCategory,on_delete=models.CASCADE, blank=True, null=True, related_name="cri_scores")

    def _university(self):
        return self.score_by_category.univ_subject.university
    _university.short_description= "University"
    
    def _subject(self):
        return self.score_by_category.univ_subject.subject
    _subject.short_description = "Subject"
    
    def update_u_score(self):
        total_score = 0
        amount = 0
        self_criterion = self.criterion
        self_category = self_criterion.category
        university = self.score_by_category.univ_subject.university
        uni_subjects = university.subject_set.all()
        for uni_subject in uni_subjects:
            try:
                cri_score_by_category = uni_subject.scores_by_category.get(category_criterion = self_category)
                cri_score = cri_score_by_category.cri_scores.get(criterion = self_criterion)
            except (SubjectScore.DoesNotExist, SubjectScoreByCategory.DoesNotExist):
                pass
            else:
                amount += 1
                total_score += cri_score.score
        uni_score_by_category, created = university.scores_by_category.get_or_create(category_criterion = self_category)
        uni_score, created = uni_score_by_category.cri_scores.get_or_create(criterion = self_criterion)
        uni_score.score = total_score / amount
        uni_score.save(update_fields=['score'])

    def update_s_score_by_category(self):
        category_cri = self.score_by_category
        cri_data = category_cri.cri_scores.all()
        cri_amount = cri_data.count()
        total_score = 0
        for cri in cri_data: 
            total_score += cri.score
        category_cri.score = total_score / cri_amount
        category_cri.save(update_fields=['score'])
        

    def save(self, univ_subject = None, *args, **kwargs):
        """
            Save SubjectScore record and update/create SubjectScoreByCategory, UniversityScore
        """
        if univ_subject is not None:
            self_category_cri = self.criterion.category
            self.score_by_category, created = univ_subject.scores_by_category.get_or_create(category_criterion = self_category_cri)
        
        if self.score_by_category is not None:
            super().save(*args, **kwargs)
            self.update_s_score_by_category()
            self.update_u_score()

    class Meta:
        db_table = "subject_score"
        ordering = ['id']
