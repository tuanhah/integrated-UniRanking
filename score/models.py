from django.db import models
from .validators import ScoreValidator

from criterion.models import CriterionCategory, Criterion


class ScoreByCriterionCategory(models.Model):
    criterion_category = models.ForeignKey(CriterionCategory, on_delete=models.CASCADE)
    score = models.FloatField(default=0, validators=[ScoreValidator(),])

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.score)

    def parse_data(self, named = False):
        parsed_criterion_category = self.criterion_category.parse_info(named = named)
        data = {"criterion_category" : parsed_criterion_category, "score" : self.score}
        return data

    def update_score(self):
        score_owner_object = self.get_score_owner_object()
        avg_score = score_owner_object.criterion_scores.filter(
                criterion__category_id = self.criterion_category_id
            ).aggregate(
                models.Avg('score')
            )
        avg_score = avg_score.get('score__avg')
        if avg_score is not None:
            self.score = round(avg_score, 2)
            self.save(update_fields = ['score'])
        else:
            self.delete()
    
    def get_score_owner_object(self):
        raise NotImplementedError("subclassess must implement this method for getting owner score object")

class ScoreByCriterion(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    score = models.FloatField(default=0, validators=[ScoreValidator(),])

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.score)

    def parse_data(self, named = False):
        parsed_criterion = self.criterion.parse_info(named = named)
        data = {"criterion" : parsed_criterion, "score" : self.score}
        return data

    def update_criterion_category_score(self):
        score_owner_object = self.get_score_owner_object()
        criterion_category_id = self.criterion.category_id
        criterion_category_score, created = score_owner_object.criterion_category_scores.get_or_create(criterion_category_id = criterion_category_id)
        criterion_category_score.update_score()
        
    def get_score_owner_object(self):
        raise NotImplementedError("subclassess must implement this method for getting owner score object")
