from django.db import models, connection

from criteria.models import Score, ScoreByCategory
from university.models import UniversitySubject, UniversityScoreByCategory

class SubjectGroup(models.Model):
    # if a subject belongs to group "Khác", it considers root_group(sector) as its direct parent on the DB
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('SubjectGroup', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')

    class Meta:
        db_table = 'subject_group'
        ordering = ['id']

    def __str__(self):
        return self.name

class Subject(models.Model):
    group = models.ForeignKey(SubjectGroup,on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'subject'
        ordering = ['id']

    def __str__(self):
        return self.name

    def sector(self):
        group = self.group
        return group if group.parent is None else group.parent



class SubjectScoreByCategory(ScoreByCategory):
    univ_subject = models.ForeignKey('university.UniversitySubject', on_delete=models.CASCADE, related_name='scores_by_category')

    class Meta: 
        db_table = 'subject_score_by_category'
        ordering = ['id']
        unique_together = ('univ_subject', 'criterion_category')
    
    def __str__(self):
        score = str(self.score)
        return 'University: {} | Subject: {} | Category: {} | Score: {}'.format(self._university(), self._subject(), self.criterion_category, score)

    def update_overall_score(self):
        self_model = self.__class__
        avg_score = self_model.objects.filter(univ_subject = self.univ_subject_id).aggregate(models.Avg('score'))
        avg_score = avg_score['score__avg'] or 0
        UniversitySubject.objects.filter(id = self.univ_subject_id).update(overall_score = round(avg_score, 2), rank = -1)
        
    def update_rank(self):
        univ_subject_table_name = UniversitySubject._meta.db_table
        subject_id = self.univ_subject.subject_id
        with connection.cursor() as cursor:
            cursor.execute('SET @rank = 0')
            cursor.execute('UPDATE {} SET rank = @rank:=(@rank + 1) WHERE subject_id = {} AND overall_score > 0 ORDER BY overall_score DESC'.format(
                univ_subject_table_name, subject_id)
            )

    def _university(self):
        return self.univ_subject.university
    _university.short_description= 'University'
    
    def _subject(self):
        return self.univ_subject.subject
    _subject.short_description = 'Subject'

class SubjectScore(Score):
    score_by_category = models.ForeignKey(SubjectScoreByCategory,on_delete=models.CASCADE, related_name='cri_scores')

    class Meta:
        db_table = 'subject_score'
        ordering = ['id']
        unique_together = ('score_by_category', 'criterion')

    def update_u_score(self):
        self_criterion = self.criterion_id
        self_criterion_category = self.score_by_category.criterion_category_id
        university_id = self.score_by_category.univ_subject.university_id

        uni_subjects = UniversitySubject.objects.filter(
            university = university_id
        ).prefetch_related(
            models.Prefetch(
                'scores_by_category',
                queryset = SubjectScoreByCategory.objects.filter(criterion_category = self_criterion_category), to_attr='cri_category_score')
        )

        cri_category_score_list = []
        for uni_subject in uni_subjects:
            if uni_subject.cri_category_score:
                cri_category_score_list.append(uni_subject.cri_category_score[0].id)
        avg_score = SubjectScore.objects.filter(score_by_category__in = cri_category_score_list, criterion = self_criterion).aggregate(models.Avg('score'))
        avg_score = avg_score.get('score__avg')

        uni_score_by_category, created = UniversityScoreByCategory.objects.filter(
            university = university_id
        ).get_or_create(
            criterion_category_id = self_criterion_category,
            defaults={'university_id' : university_id}
        )
        uni_score, created = uni_score_by_category.cri_scores.get_or_create(criterion_id = self_criterion)
        if avg_score is not None:
            uni_score.score = round(avg_score, 2)
            uni_score.save(update_fields=['score'])
        else:
            uni_score.delete()

    def _university(self):
        return self.score_by_category.univ_subject.university
    _university.short_description= "University"
    
    def _subject(self):
        return self.score_by_category.univ_subject.subject
    _subject.short_description = "Subject"