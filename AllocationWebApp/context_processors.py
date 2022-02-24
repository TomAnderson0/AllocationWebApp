from django.shortcuts import get_object_or_404
from .models import UserProfile, User
from django.contrib.auth.decorators import login_required

def dictionary(request):
    if(request.user.id):
        user = get_object_or_404(User, username=request.user.username)
        user_profile = get_object_or_404(UserProfile, user=user)
        user_type = user_profile.user_type

        user_instance = user_profile.instance
        instance_stage = user_instance.stage

        return {'user_type': user_type, 'instance_stage': instance_stage}
    return {}