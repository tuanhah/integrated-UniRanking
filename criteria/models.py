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
    score_by_category = "A foreign key to a score by category table, be defined in the child class"

    def update_score_by_category(self):
        category_cri_score = self.score_by_category
        cri_data = category_cri_score.cri_scores.all()
        cri_amount = cri_data.count()
        total_score = 0
        if cri_amount > 0:
            for cri in cri_data: 
                total_score += cri.score
            category_cri_score.score = total_score / cri_amount
            category_cri_score.save(update_fields=['score'])
        else:
            category_cri_score.delete()

    def __str__(self):
        return str(self.score)

    class Meta:
        abstract = True