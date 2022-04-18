from django.shortcuts import render, redirect

# showing message, e.x. after a successful registration
from django.contrib import messages

# to use our own forms for user creation etc. (look --> forms.py)
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# to access to the pages only if a user is logged in
from django.contrib.auth.decorators import login_required


# we make a function to deal with user requests
def register(request):
    # when a user fullfils the login form in the web-page and
    # clicks to a submit button, he produces a POST-request.
    # In this case he instantiates a form which has passed all POST-data into the UserCreationForm
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # -> POST data was passed into UserCreationForm
        if form.is_valid():
            # save data into form
            form.save()
            username = form.cleaned_data.get('username') # converting data from form to Pythonic data
            # create success message
            messages.success(request, f'Your account has been created! You are now able to log in.')
            # redirect to home page
            return redirect('login') # 'home' --> look at urls pattern in myboardapp
    else:
        # otherwise, when the page is loaded first time, probably by GET-request
        # it crates an blank form
        form = UserRegisterForm()
    # and returns us a rendered form on the same page
    # also, if a user posted invalid data into a form, form will add error messages when returns page
    return render(request, 'users/register.html', {'form': form})


@login_required # user must be logged in to access this page
def profile(request):
    # user profile update form
    if request.method == 'POST':
        # update user fields form
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # update user's picture form
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            # redirect to profile page
            return redirect('profile') # GET request

    else:
        # show existing fields' values in the form
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
    }

    # return on the page the form as content with context
    return render(request, 'users/profile.html', context)