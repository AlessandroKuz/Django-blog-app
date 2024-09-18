from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form_instance = UserRegisterForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            username = form_instance.cleaned_data.get('username')
            messages.success(request, f"Successfully created Account for {username}! You can now login")
            return redirect('login')
        # else:
            # messages.error
    else:
        form_instance = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form_instance})

@login_required  # makes it so the user gets redirected to login page if not authenticated
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST,
                                                request.FILES,
                                                instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f"Your Account has been successfully updated")
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'users/profile.html', context)
