from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from accounts.forms import UserProfileForm

def retrieve_or_create(request):
    '''Retrieve or create a user profile.'''
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return profile

def update(request):
    '''Update user profile using form data.'''
    profile = retrieve_or_create(request)
    profile_form = UserProfileForm(request.POST, instance=profile)

    if profile_form.is_valid():
        profile_form.save()
