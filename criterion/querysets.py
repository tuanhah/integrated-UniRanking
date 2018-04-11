from django.db.models import QuerySet

class CriterionCategoryQueryset(QuerySet):
    def university_only(self):
        return self.filter(university_only = True)
    def subject_only(self):
        return self.exclude(university_only = True)

class CriterionQueryset(QuerySet):
    def university_only(self):
        return self.filter(category__university_only = True)

    def subject_only(self):
        return self.exclude(category__university_only = True)