from django.views import View
# from django.http import JsonResponse

class BaseManageView(View):
    """
    The base class for ManageViews
    A ManageView is a view which is used to dispatch the requests to the appropriate views
    This is done so that we can use one URL with different methods (GET, PUT, etc)
    """

    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method](request, *args, **kwargs)
        return JsonResponse({},status = 405)
    

class ScoreListView(BaseManageView):
    class ScoresFiltering:
        ALL_SCORES = '0'
        ONLY_CATEGORY_SCORES = '1'
        ONLY_CRITERION_SCORES = '2'

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_scores,
        }


class ScoreDetailView(BaseManageView):
    class ScoresFiltering:
        ALL_SCORES = 'all'
        ONLY_CATEGORY_SCORES = 'category'
        ONLY_CRITERION_SCORES = 'criterion'

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_scores,
            'POST' : self.add_score,
            'PUT' : self.edit_score,
            'DELETE' : self.delete_score, 
        }