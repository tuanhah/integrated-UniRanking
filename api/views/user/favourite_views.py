from django.http import JsonResponse
from django.db.models import Prefetch, Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from guardian.decorators import permission_required_or_403
from django.contrib.auth.models import User
from university.models import University, UserFavouriteUniversity
from api.views.base import BaseManageView
from api.functions import string_to_boolean

class FavouriteUniversityListView(BaseManageView):
    """
        List all favourite Universities of an user

    """
    error_messages = {
        "user": {
            "invalid": "This user is invalid",
            "required": "User is required"
        }
    }

    def __init__(self, *args, **kwargs):
        self.VIEWS_BY_METHOD = {
            'GET' : self.get_universities,
        }
    
    def get_universities(self, request):
        request_data = request.GET
        user_id = request_data.get('user')
        if user_id is None:
            return self.json_error(field="user", code="required")
        else:
            if not user_id.isdigit():
                return self.json_error(field="user", code="invalid")
            else:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return self.json_error(field="user", code="invalid")
                else:
                    universities_queryset = user.favourite_university_set.all()
        result = {"favourite_universities" : [university.parse_full_profile() for university in universities_queryset]}
        return JsonResponse(result)
