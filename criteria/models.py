from django.db import models

class CategoryCriterion(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "category_criterion"
        ordering = ['id']

class Criterion(models.Model):
    category = models.ForeignKey(CategoryCriterion, on_delete=models.CASCADE, related_name="criteria")
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "criterion"
        ordering = ['id']

class ScoreByCategory(models.Model):
    category_criterion = models.ForeignKey(CategoryCriterion, on_delete=models.CASCADE, null=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return str(self.score)

    class Meta:
        abstract = True

class Score(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, null=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return str(self.score)

    class Meta:
        abstract = True