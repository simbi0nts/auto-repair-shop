
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from core.forms import UserRegisterForm, UserUpdateForm, UserCarUpdateForm
from core.models import UserCar


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your account has been created! You are now able to log in'))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile(request):
    user_car, is_created = UserCar.objects.get_or_create(owner=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        user_car_form = UserCarUpdateForm(request.POST,
                                          request.FILES,
                                          instance=user_car)
        if user_form.is_valid() and user_car_form.is_valid():
            user_form.save()
            user_car_form.save()
            messages.success(request, _('Your account has been updated!'))
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        user_car_form = UserCarUpdateForm(instance=user_car)

    context = {
        'user_form': user_form,
        'user_car_form': user_car_form
    }

    return render(request, 'user/profile.html', context)
