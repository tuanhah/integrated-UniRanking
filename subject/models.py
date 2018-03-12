from django.db import models
from criteria.models import Score, ScoreByCategory

class GroupSubject(models.Model):
    # if a subject belongs to group "Khác", it considers root_group as its direct parent on DB
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('GroupSubject', on_delete=models.SET_NULL, null=True, blank=True, related_name="groups")

    class Meta:
        db_table = "group_subject"
        ordering = ['id']

    def __str__(self):
        return self.name

class Subject(models.Model):
    group = models.ForeignKey(GroupSubject,on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=50)

    def root_group(self):
        group = self.group
        return group.name if group.parent is None else group.parent.name

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "subject"
        ordering = ['id']


class SubjectScoreByCategory(ScoreByCategory):
    univ_subject = models.ForeignKey('university.UniversitySubject', on_delete=models.CASCADE, related_name="scores_by_category")

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                self.univ_subject.scores_by_category.get(category_criterion = self.category_criterion)
            except SubjectScoreByCategory.DoesNotExist:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

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
        if amount > 0:
            uni_score.score = total_score / amount
            uni_score.save(update_fields=['score'])
        else:
            uni_score.delete()
        
    def save(self, univ_subject = None, *args, **kwargs):
        """
            Save SubjectScore record and update/create SubjectScoreByCategory, UniversityScore
        """
        if self.pk is None: #for creating new object
            try:
                existed_subj_score = self.score_by_category.cri_scores.get(criterion = self.criterion)
            except SubjectScore.DoesNotExist:
                super().save(*args, **kwargs)
            else:
                existed_subj_score.score = self.score
                existed_subj_score.save(update_fields = ["score"])
        else: #for editing object
            super().save(*args, **kwargs)
        
        self.update_score_by_category()
        self.update_u_score()

        #update parent university score
    
    def delete(self):
        super().delete()
        self.update_score_by_category()
        self.update_u_score()

    class Meta:
        db_table = "subject_score"
        ordering = ['id']
