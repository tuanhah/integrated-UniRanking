from collections import OrderedDict

class ScoreUnit:
    """
        Group CriterionCategoryScore with its CriterionScores
        ScoreUnit object stores:
            One CriterionCategoryScore object
            List of CriterionScore objects which are all point to CriterionCategoryScore above
    """

    def __init__(self, criterion_category_score = None, criterion_scores = None):
        super().__init__()
        self.criterion_category_score = criterion_category_score
        if isinstance(criterion_scores, list):
            self.criterion_scores = criterion_scores
        else:
            self.criterion_scores = []
            
    def set_criterion_category_score(self, criterion_category_score):
        self.criterion_category_score = criterion_category_score

    def append_criterion_score(self, criterion_score):
        self.criterion_scores.append(criterion_score)
    
    def parse_data(self, named = False):
        parsed_criterion_category_score = self.parse_criterion_category_score(named = named)
        parsed_criterion_score_list = self.parse_criterion_scores(named = named) 
        data = {"criterion_category_score" : parsed_criterion_category_score, "criterion_scores" : parsed_criterion_score_list}
        return data

    def parse_criterion_category_score(self, named = False):
        parsed_criterion_score = self.criterion_category_score.parse_data(named = named)
        return parsed_criterion_score
    
    def parse_criterion_scores(self, named = False):
        parsed_criterion_score_list = [criterion_score.parse_data(named = named) for criterion_score in self.criterion_scores]
        return parsed_criterion_score_list

    def __str__(self): 
        return str(self.criterion_category_score)

class ScoreContainer:
    """
        Get scores from db and stores in ScoreUnit list
    """ 

    def __init__(self, score_owner_instance):
        super().__init__()
        self.score_owner_instance = score_owner_instance
        self.container = OrderedDict()
        self.criterion_category_scores_are_fetched = False
        self.criterion_scores_are_fetched = False

    def all_scores__db_to_container(self):
        self.criterion_category_scores__db_to_container()
        self.criterion_scores__db_to_container()
        
    def criterion_category_scores__db_to_container(self): 
        criterion_category_scores = self.score_owner_instance.criterion_category_scores.all()
        for criterion_category_score in criterion_category_scores:
            criterion_category_id = criterion_category_score.criterion_category_id
            score_unit = ScoreUnit(criterion_category_score = criterion_category_score)
            self.container.update({criterion_category_id : score_unit})
        
        self.criterion_category_scores_are_fetched = True

    def criterion_scores__db_to_container(self):
        criterion_scores = self.score_owner_instance.criterion_scores.all()
        for criterion_score in criterion_scores:
            criterion_category_id = criterion_score.criterion.category_id
            score_unit = self.container[criterion_category_id]
            score_unit.append_criterion_score(criterion_score)

        self.criterion_scores_are_fetched = True

    def criterion_category_scores_to_list(self):
        if not self.criterion_category_scores_are_fetched:
            self.criterion_category_scores__db_to_container()
        criterion_category_score_list = [score_unit.criterion_category_score for score_unit in self.container.values()]
        return criterion_category_score_list

    def all_scores_to_list(self):
        if not self.criterion_category_scores_are_fetched and not self.criterion_scores_are_fetched:
            self.all_scores__db_to_container()
        score_list = list(self.container.values())
        return score_list