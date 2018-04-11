from itertools import groupby

class UniversitySubjectParserMixin: 
    """
        Mixin that provides method for parsing subjects from specific university
    """

    def parse_sorted_university_subjects(self):
        data = []
        sorted_subjects = self.subjects.select_related("group__sector")    
        sorted_subjects = sorted(sorted_subjects, key = lambda s : s.sector.id)
        iter = groupby(sorted_subjects, key = lambda s : s.sector)
        for sector, subjects in iter:
            parsed_sector = sector.parse_profile()
            inner_iter = groupby(subjects, key = lambda s : s.group)
            group_list = []
            for group, inner_subjects in inner_iter:
                parsed_group = group.parse_profile()
                parsed_subject_list = group.parse_all_subject_profiles()
                group_list.append({"group" : parsed_group, "subjects" : parsed_subject_list})
            data.append({"sector" : parsed_sector , "groups" : group_list})
        return data

    def parse_university_subjects_of_group(self, group):
        subject_queryset = self.subjects.filter(group = group)
        subject_list = [subject.parse_profile() for subject in subject_queryset]
        return subject_list