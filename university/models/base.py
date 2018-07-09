from django.db import models, connection
from django.urls import reverse

from score.querysets import ScoreOwnerQueryset
from university.mixins import UniversitySubjectParserMixin
from score.mixins import ScoreOwnerMixin, ScoreParserMixin

class University(models.Model, ScoreOwnerMixin, UniversitySubjectParserMixin, ScoreParserMixin):
    code = models.CharField(max_length=7, null=True, unique = True)
    name = models.CharField(max_length=100)
    image_path = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('University', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_universities')
    # subjects = models.ManyToManyField('subject.Subject', through='subject.UniversitySubject')
    sector = models.ManyToManyField('subject.Sector', through='subject.UniversitySector')
    avg_score = models.FloatField(default=0)
    rank = models.IntegerField(default=-1)
    
    objects = ScoreOwnerQueryset.as_manager()

    class Meta:
        db_table = 'university'
        ordering = ['id']   

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('university_profile', kwargs={'id': self.pk})

    def parse_profile(self):
        data= {
            "university" : self.parse_basic_info(),
            "general_statistics" : self.parse_general_statistics() 
        }
        return data

    def parse_full_profile(self):
        data = self.parse_profile()
        detail = self.profile
        data["university"].update({
            "overview" : detail.overview,
            "site_url" : detail.site_url,
            "address" : detail.address,
        })
        return data

    def parse_basic_info(self):
        data = {
            "id" : self.id,
            "name" : self.name,
            "image_href" : self.image_path,
            "site_href" : self.get_absolute_url(),
        }
        return data

    def get_avg_score(self):
        avg_score = self.criterion_category_scores.aggregate(models.Avg('score'))
        avg_score = avg_score['score__avg'] or 0
        return avg_score        

    def update_rank(self):
        university_table_name = self._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute('SET @rank = 0')
            cursor.execute('UPDATE {0} SET rank = @rank:=(@rank + 1) WHERE {1} > 0 ORDER BY {1} DESC'.format(
                university_table_name, "avg_score")
            )

    def create_university_profile_object(self):
        UniversityProfile.objects.create(university_id = self.id)


class UniversityProfile(models.Model):
    university = models.OneToOneField(University, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    overview = models.TextField(blank = True, null=True)
    site_url = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'university_profile'
        ordering = ['university']   

    def __str__(self):
        return self.university.name