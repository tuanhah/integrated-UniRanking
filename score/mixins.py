from score.containers import ScoreContainer

class ScoreOwnerMixin:
    def update_avg_score_and_rank(self):
        self.avg_score = self.get_avg_score()
        self.reset_rank()
        self.save()
        self.update_rank()

    def get_avg_score(self):
        raise NotImplementedError("subclasses must implemenet get_avg_score()")

    def reset_rank(self):
        self.rank = -1

    def update_rank(self):
        raise NotImplementedError("subclasses must implemenet update_rank()")

    def parse_general_statistics(self):
        data = {
            "avg_score" : self.avg_score,
            "rank" : self.rank
        }
        return data

class ScoreParserMixin:
    """
        Mixin that provides method for parsing score data from University/UniversitySubject model
    """

    def parse_data(self, named = False):
        data = {
            "profile" : self.parse_profile(),
            "scores" : self.parse_scores(named = named)
        }
        return data
        
    def parse_profile(self):
        raise NotImplementedError("subclasses of ScoreParserMixin must provide an parse_profile() method")

    def parse_general_statistics(self):
        data = {
            "overall_score" : self.overall_score,
            "rank" : self.rank
        }
        return data

    def parse_scores(self, named = False):
        if not hasattr(self, "score_container"):
            self.initialize_score_container()
        score_unit_list = self.score_container.all_scores_to_list()
        parsed_scores = [score_unit.parse_data(named = named) for score_unit in score_unit_list]
        return parsed_scores

    def parse_criterion_category_scores(self, named = False):
        if not hasattr(self, "score_container"):
            self.initialize_score_container()
        criterion_category_scores = self.score_container.criterion_category_scores_to_list()
        parsed_scores = [criterion_category_score.parse_data(named = named) for criterion_category_score in criterion_category_scores]
        return parsed_scores

    def initialize_score_container(self):
        self.score_container = ScoreContainer(self)