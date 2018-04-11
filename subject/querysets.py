from django.db.models import QuerySet

class SubjectGroupQueryset(QuerySet):
    def sectors(self):
        return self.filter(sector_id = None)
    
    def groups(self):
        return self.exclude(sector_id = None)