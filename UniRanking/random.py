from random import randint, choice
from django.core.exceptions import ValidationError

from university.models import University, UniversityScoreByCriterion
from subject.models import Subject, UniversitySubject, SubjectScoreByCriterion
from criterion.models import Criterion

def frange(start, end, step):
    tmp = start
    while tmp <= end: 
        yield tmp
        tmp += step

def random_ignore_amount(max_amount):
        return randint(0, max_amount)

def fake_university(university_id):
    UniversitySubjectRandom(university_id).random()
    CriterionScoreRandom(university_id).random()
    
class CriterionScoreRandom:
    error_messages = {
        "university" : "university_id is invalid",
        "max_ignore_university_criteria" : "max_ignore_university_criteria must be instance of int and gte than 0 and lte thanuniversity criterion amount",
        "max_ignore_subject_criteria" : "max_ignore_subject_criteria must be instance of int and gte than 0 and lte than subject criterion amount "
    }
    
    def __init__(self, university_id, max_ignore_university_criteria = 1, max_ignore_subject_criteria = 3):
        self.set_university(university_id)
        self.university_subjects = UniversitySubject.objects.filter(university = self.university)

        self.university_only_criteria = Criterion.objects.university_only().values_list("id", flat = True)
        self.set_max_ignore_university_criteria(max_ignore_university_criteria)
        
        self.subject_only_criteria = Criterion.objects.subject_only().values_list("id", flat = True)
        self.set_max_ignore_subject_criteria(max_ignore_subject_criteria)
    
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
                (max_ignore_university_criteria >= 0 and max_ignore_university_criteria <= len(self.university_only_criteria))
           ):
            self.max_ignore_university_criteria = max_ignore_university_criteria
        else:
            raise ValidationError(self.error_messages["max_ignore_university_criteria"])

    def set_max_ignore_subject_criteria(self, max_ignore_subject_criteria):
        if (
            isinstance(max_ignore_subject_criteria, int) 
            and (max_ignore_subject_criteria >= 0 and max_ignore_subject_criteria <= len(self.subject_only_criteria))
           ):
            self.max_ignore_subject_criteria = max_ignore_subject_criteria
        else:
            raise ValidationError(self.error_messages["max_ignore_subject_criteria"])

    def random(self):
        self.random_university_criterion_scores()
        self.random_all_subject_criterion_scores()
    
    def random_university_criterion_scores(self):
        criteria = self.random_criteria(score_owner = self.university, criteria = self.university_only_criteria, max_ignore_criteria = self.max_ignore_university_criteria)
        for criterion_id in criteria:
            score = self.random_score()
            UniversityScoreByCriterion.objects.create(university = self.university, criterion_id = criterion_id, score = score)
        
    def random_all_subject_criterion_scores(self):
        for university_subject in self.university_subjects:
            self.random_subject_criterion_scores(university_subject)

    def random_subject_criterion_scores(self, university_subject):
        criteria = self.random_criteria(score_owner = university_subject, criteria = self.subject_only_criteria, max_ignore_criteria = self.max_ignore_subject_criteria)
        for criterion_id in criteria:
            score = self.random_score()
            SubjectScoreByCriterion.objects.create(univ_subject = university_subject, criterion_id = criterion_id, score = score)
    
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

class UniversitySubjectRandom:
    error_messages = {
        "university" : "university_id is invalid",
        "max_ignore_subjects" : "max_subjects must be instance of int and gte than 0 and lte than subject amount",
    }
    
    def __init__(self, university_id, max_random_subjects = 20):
        self.set_university(university_id)
        self.subjects = Subject.objects.values_list("id", flat = True)
        self.set_max_random_subjects(max_random_subjects)

    def set_university(self, university_id):
        if isinstance(university_id, int):
            try:
                self.university = University.objects.get(id = university_id)
            except University.DoesNotExist:
                raise ValidationError(self.error_messages["university"])
        else:
            raise ValidationError(self.error_messages["university"])

    def set_max_random_subjects(self, max_random_subjects):
        if (
                isinstance(max_random_subjects, int) and
                (max_random_subjects >= 0 and max_random_subjects <= len(self.subjects))
           ):
            self.max_random_subjects = max_random_subjects
        else:
            raise ValidationError(self.error_messages["max_random_subjects"])

    def random(self):
        random_subject_id_list = self.random_subject_id_list()
        UniversitySubject.objects.bulk_create([UniversitySubject(university = self.university, subject_id = subject_id) for subject_id in random_subject_id_list])
    
    def random_subject_id_list(self):
        random_subject_id_list = set()
        for i in range(self.max_random_subjects):
            while True:
                subject_id = choice(self.subjects)
                if subject_id not in random_subject_id_list:
                    random_subject_id_list.add(subject_id)
                    break
                else: 
                    continue
        added_subject = set(self.university.subjects.values_list("id", flat = True))
        return random_subject_id_list - added_subject
                    

        

