from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.contrib import auth
from django.template import RequestContext
from django.template.context_processors import csrf
from django.urls import reverse

from accounts.forms import RegistrationForm, EditProfileForm, EditProfileMore
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required



def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()
    if request.POST:
        newuser_form = RegistrationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'],
                                        first_name=newuser_form.cleaned_data['first_name'],
                                        last_name=newuser_form.cleaned_data['last_name'],
                                        email=newuser_form.cleaned_data['email'],
                                        )
            auth.login(request, newuser)
            return redirect(reverse('home:home'))
        else:
            args['form'] = newuser_form
    return render_to_response('accounts/register.html', args)


def profile(request, pk=None):
    storege = messages.get_messages(request)
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user, 'message': storege}
    return render(request, 'accounts/profile.html', args)



@login_required
def edit_profile(request):
    if request.method == 'POST':
        epf = EditProfileForm(request.POST, instance=request.user)
        epm = EditProfileMore(request.POST, instance=request.user.userprofile)
        if epf.is_valid() and epm.is_valid():
            epf.save()
            epm.save()
            messages.success(request, ('Your profile was successfully update!'))
            return redirect('/account/profile')
        else:
            messages.error(request, ('Please correct the error below!'))
    else:
        epf = EditProfileForm(instance=request.user)
        epm = EditProfileMore(instance=request.user.userprofile)
        args = {'form1': epf, 'form2': epm}
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your new password has been saved.')
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        # else:
        #     return redirect('/account/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)