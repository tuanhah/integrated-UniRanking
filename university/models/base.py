from django.db import models, connection
from django.urls import reverse
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm, remove_perm

from score.querysets import ScoreOwnerQueryset
from university.mixins import UniversitySubjectParserMixin
from score.mixins import ScoreOwnerMixin, ScoreParserMixin
from django.utils.translation import gettext as _

class University(models.Model, ScoreOwnerMixin, UniversitySubjectParserMixin, ScoreParserMixin):
    code = models.CharField(max_length=7, null=True, unique = True, verbose_name=_('Code'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    image_path = models.TextField(blank=True, null=True, verbose_name=_('Image_path'))
    avatar_path = models.TextField(blank=True, null=True, verbose_name=_('Avatar_path'))
    parent = models.ForeignKey('University', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_universities', verbose_name=_('Parent University'))
    sectors = models.ManyToManyField('subject.Sector', through='subject.UniversitySector')
    favourite_users = models.ManyToManyField('auth.User', through='university.UserFavouriteUniversity', related_name="favourite_university_set")
    manage_users = models.ManyToManyField('auth.User', through='university.UserManagerUniversity', related_name="manage_university_set")    
    avg_score = models.FloatField(default=0, verbose_name=_('Average Score'))
    rank = models.IntegerField(default=-1, verbose_name=_('Rank'))
    
    objects = ScoreOwnerQueryset.as_manager()

    class Meta:
        db_table = 'university'
        ordering = ['id']
        verbose_name = _('University')
        verbose_name_plural = _('Universities')
        permissions = (
        )

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
            "avatar_href": self.avatar_path,
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
    university = models.OneToOneField(University, on_delete=models.CASCADE, primary_key=True, related_name="profile", verbose_name=_('University'))
    overview = models.TextField(blank = True, null=True, verbose_name=_('Overview'))
    site_url = models.URLField(blank=True, null=True, verbose_name=_("Site's URL"))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))

    class Meta:
        db_table = 'university_profile'
        ordering = ['university']   
        verbose_name = _('University Profile')   
        verbose_name_plural = _('Universities Profile')   
        
    def __str__(self):
        return self.university.name

class UserFavouriteUniversity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_universities_set', verbose_name=_('User'))
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='favourite_users_set', verbose_name=_('University'))
    
    class Meta:
        db_table = 'user_favourite_university'
        ordering = ['id']
        unique_together = ('user', 'university')
        verbose_name = _('User - Favourite University')
        verbose_name_plural = _('User - Favourite Universities')        

    def __str__(self):
        return _("User: {} | University: {}".format(self.user, self.university.name))


class UserManagerUniversity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_universities_set', verbose_name=_('User'))
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='manager_users_set', verbose_name=_('University'))
    
    class Meta:
        db_table = 'user_manager_university'
        ordering = ['id']
        unique_together = ('user', 'university')
        verbose_name = _('User - Manager University')
        verbose_name_plural = _('User - Manager Universities')        

    def __str__(self):
        return _("User: {} | University: {}".format(self.user, self.university.name))

    def add_permissions(self):
        user = self.user
        university = self.university
        assign_perm('change_university', user, university)

    def remove_permissions(self):
        user = self.user
        university = self.university
        remove_perm("change_university", user, university)
