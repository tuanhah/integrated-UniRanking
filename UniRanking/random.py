from random import randint, choice
from django.core.exceptions import ValidationError

from university.models import University, UniversityScoreByCriterion
from subject.models import Sector, UniversitySector
from criterion.models import Criterion

def frange(start, end, step):
    tmp = start
    while tmp <= end: 
        yield tmp
        tmp += step

def random_ignore_amount(max_amount):
        return randint(0, max_amount)

def fake_university(university_id):
    UniversitySectorRandom(university_id).random()
    CriterionScoreRandom(university_id).random()
    
class CriterionScoreRandom:
    error_messages = {
        "university" : "university_id is invalid",
        "max_ignore_university_criteria" : "max_ignore_university_criteria must be instance of int and gte than 0 and lte thanuniversity criterion amount",
        "max_ignore_sector_criteria" : "max_ignore_sector_criteria must be instance of int and gte than 0 and lte than sector criterion amount "
    }
    
    def __init__(self, university_id, max_ignore_university_criteria = 1, max_ignore_sector_criteria = 3):
        self.set_university(university_id)
        self.university_sectors = UniversitySector.objects.filter(university = self.university)

        self.all_criteria = Criterion.objects.all().values_list("id", flat = True)
        self.set_max_ignore_university_criteria(max_ignore_university_criteria)
        
        self.all_criteria = Criterion.objects.all().values_list("id", flat = True)
        self.set_max_ignore_sector_criteria(max_ignore_sector_criteria)
    
    def set_university(self, university_id):
        if isinstance(university_id, int):
            try:
                self.university = University.objects.get(id = university_id)
            except University.DoesNotExist:
                raise ValidationError(self.error_messages["university"])
        else:
            raise ValidationError(self.error_messages["university"])

    def set_max_ignore_university_criteria(self, max_ignore_university_criteria):
        if (
                isinstance(max_ignore_university_criteria, int) and
                (max_ignore_university_criteria >= 0 and max_ignore_university_criteria <= len(self.all_criteria))
           ):
            self.max_ignore_university_criteria = max_ignore_university_criteria
        else:
            raise ValidationError(self.error_messages["max_ignore_university_criteria"])

    def set_max_ignore_sector_criteria(self, max_ignore_sector_criteria):
        if (
            isinstance(max_ignore_sector_criteria, int) 
            and (max_ignore_sector_criteria >= 0 and max_ignore_sector_criteria <= len(self.all_criteria))
           ):
            self.max_ignore_sector_criteria = max_ignore_sector_criteria
        else:
            raise ValidationError(self.error_messages["max_ignore_sector_criteria"])

    def random(self):
        self.random_university_criterion_scores()
        # self.random_all_sector_criterion_scores()
    
    def random_university_criterion_scores(self):
        criteria = self.random_criteria(score_owner = self.university, criteria = self.all  _criteria, max_ignore_criteria = self.max_ignore_university_criteria)
        for criterion_id in criteria:
            score = self.random_score()
            UniversityScoreByCriterion.objects.create(university = self.university, criterion_id = criterion_id, score = score)
        
    def random_criteria(self, score_owner, criteria, max_ignore_criteria):
        ignore_amount = random_ignore_amount(max_ignore_criteria)
        random_criteria = list(criteria) #for support random choice 
        for i in range(ignore_amount):
            criterion = choice(random_criteria)
            random_criteria.remove(criterion)
        random_criteria = set(random_criteria)
        added_criteria = set(score_owner.criterion_scores.filter(criterion_id__in = random_criteria).values_list("criterion_id", flat = True))
        return random_criteria - added_criteria

    def random_score(self):
        valid_score_list = list(frange(1, 10, 0.25))
        random_score = choice(valid_score_list)
        return random_score

class UniversitySectorRandom:
    error_messages = {
        "university" : "university_id is invalid",
        "max_ignore_sectors" : "max_sectors must be instance of int and gte than 0 and lte than sector amount",
    }
    
    def __init__(self, university_id, max_random_sectors = 20):
        self.set_university(university_id)
        self.sectors = Sector.objects.values_list("id", flat = True)
        self.set_max_random_sectors(max_random_sectors)

    def set_university(self, university_id):
        if isinstance(university_id, int):
            try:
                self.university = University.objects.get(id = university_id)
            except University.DoesNotExist:
                raise ValidationError(self.error_messages["university"])
        else:
            raise ValidationError(self.error_messages["university"])

    def set_max_random_sectors(self, max_random_sectors):
        if (
                isinstance(max_random_sectors, int) and
                (max_random_sectors >= 0 and max_random_sectors <= len(self.sectors))
           ):
            self.max_random_sectors = max_random_sectors
        else:
            raise ValidationError(self.error_messages["max_random_sectors"])

    def random(self):
        random_sector_id_list = self.random_sector_id_list()
        UniversitySector.objects.bulk_create([UniversitySector(university = self.university, sector_id = sector_id) for sector_id in random_sector_id_list])
    
    def random_sector_id_list(self):
        random_sector_id_list = set()
        for i in range(self.max_random_sectors):
            while True:
                sector_id = choice(self.sectors)
                if sector_id not in random_sector_id_list:
                    random_sector_id_list.add(sector_id)
                    break
                else:
                    continue
        added_sector = set(self.university.sector.values_list("id", flat = True))
        return random_sector_id_list - added_sector
                    

        

