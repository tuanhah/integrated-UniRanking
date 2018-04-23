from django.db import models, connection

from score.models import ScoreByCriterionCategory, ScoreByCriterion
from score.querysets import ScoreOwnerQueryset
from university.models import University
from score.mixins import ScoreOwnerMixin, ScoreParserMixin
from subject.querysets import SubjectGroupQueryset

class SubjectGroup(models.Model):
    # if a subject belongs to group "Khác", it considers root_group(sector) as its direct parent on the DB
    name = models.CharField(max_length=100)
    sector = models.ForeignKey('SubjectGroup', on_delete=models.SET_NULL, null=True, blank=True, related_name='groups')

    objects = SubjectGroupQueryset.as_manager()

    class Meta:
        db_table = 'subject_group'
        ordering = ['id']

    def __str__(self):
        name = self.name
        if name == "Khác": 
            name += " ({})".format(self.sector)
        return name

    def is_sector(self):
        return not self.is_group()
    is_sector.short_description = "SECTOR"
    is_sector.boolean = True

    def is_group(self):
        return self.sector_id is not None
    is_group.short_description = "Group"
    is_group.boolean = True

    def is_group_of_sector(self, sector_id):
        return self.sector_id == sector_id

    def parse_profile(self):
        data = {"id" : self.id, "name" : self.name}
        return data

    def parse_all_subject_profiles(self):
        subjects = self.subjects.all()
        parsed_subjects = [subject.parse_profile() for subject in subjects]
        return parsed_subjects

class Subject(models.Model):
    group = models.ForeignKey(SubjectGroup,on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'subject'
        ordering = ['id']

    def __str__(self):
        return self.name

    @property
    def sector(self):
        return self.group.sector

    def parse_profile(self):
        data = {"id" : self.id, "name" : self.name}
        return data

class UniversitySubject(models.Model, ScoreOwnerMixin, ScoreParserMixin):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='subject_set')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='universities')
    avg_score = models.FloatField(default=0, blank=True)
    rank = models.IntegerField(default=-1, blank=True)

    objects = ScoreOwnerQueryset.as_manager()

    class Meta:
        db_table = 'university_subject'
        ordering = ['id']
        unique_together = ('university', 'subject')
    
    def __str__(self):
        return "University: {} | Subject: {}".format(self.university.name, self.subject.name)

    def get_absolute_url(self):
        return reverse('university_profile', kwargs={'id': self.id})

    def parse_basic_info(self):
        data = {
            "university" : self.university.parse_basic_info(),
            "subject" : self.subject.parse_profile(),
        }
        return data

    def parse_profile(self):
        data = self.parse_basic_info() 
        data.update({
            "general_statistics" : self.parse_general_statistics()
        })  
        return data

    def get_avg_score(self):
        avg_score = self.criterion_category_scores.aggregate(models.Avg('score'))
        avg_score = avg_score['score__avg'] or 0
        return avg_score

    def update_rank(self):
        univ_subject_table_name = self._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute('SET @rank = 0')
            cursor.execute('UPDATE {0} SET rank = @rank:=(@rank + 1) WHERE subject_id = {1} AND {2} > 0 ORDER BY {2} DESC'.format(
                univ_subject_table_name, self.subject_id, "avg_score")
            )