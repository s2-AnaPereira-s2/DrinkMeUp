import random
from django.contrib import messages
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView, TemplateView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from pathlib import Path
from .forms import BarUserForm
from .models import UserProfile, Drinks, DrinksMade
from pathlib import Path



# Create utilities here
def get_file_content_as_list(path_file: str) -> list:
    """Returns content of a file as a list of strings one string per line"""
    try:
        with open(path_file) as f:
            content = f.readlines()
    except FileNotFoundError as err:
        print(err)
    return content    


BASE_DIR = Path(__file__).resolve().parent 
RESPONSE_FILE = BASE_DIR / "templates/tough_responses.txt"


## Password Reset
class CustomPasswordResetView(PasswordResetView):
    """Allows user to reset password if forgotten"""
    template_name = "registration/custom_password_reset_form.html"
    email_template_name = "registration/custom_password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Informs the user if password reset was successfull"""
    template_name = "registration/custom_password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """This view uses a custom template to display the password reset confirmation form."""
    template_name = "registration/custom_password_reset_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """This view uses a custom template to display the password reset completion message."""
    template_name = "registration/custom_password_reset_complete.html"


class CustomPasswordChangeView(PasswordChangeView):
    """This view uses a custom template to display the password change form."""
    template_name = "registration/change_password.html"


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    """This view uses a custom template to display the password change success message."""
    template_name = "registration/change_password_done.html"


class CustomLoginView(LoginView):
    """This view uses a custom template to display the login form."""
    template_name = "registration/login.html"

## Signup
def signup_view(request):
    """View that lets the user signup to the page. Sends a welcome mail upon successfull signup"""
    if request.method == "POST":
        form = BarUserForm(request.POST)
        if form.is_valid():  
            username = form.cleaned_data.get("username")                # create the new user
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            user = User.objects.create_user(username=username, email=email, password=password)  
            user_profile = UserProfile.objects.create(user=user)               # create userinfo related to new user
            user.backend = "django.contrib.auth.backends.ModelBackend"  # Choose correct backend for user creation -> settings/AUTHENTICATION_BACKENDS
            login(request, user)    
            return redirect("profile")
        else:
            return render(request, "registration/signup.html", {"form":form})
    else: 
        form = BarUserForm()
    return render(request, "registration/signup.html", {"form":form})


#logout functionality
def logout_endpoint(request):
    """Logs out the user"""
    logout(request)
    return redirect('/')


@login_required
def delete_user_func(request):
    """Let the user delete his profile"""
    username = request.user.username
    if request.method == 'POST':
        user_id = request.user.id
        user_to_delete = User.objects.filter(pk=user_id)
        delete_user_drinks = DrinksMade.objects.filter(user=username)
        delete_user_drinks.delete()
        user_to_delete.delete()
        
        return redirect('login')
    return render(request, "bar_pedro/delete.html", {'member': username})


@login_required
def profile_view(request):
    """here the user information is displayed in the profile page and user is able to answer some questions so it can suggest cocktails"""
    
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    latest_post =  user_profile.latest_post
    user_drinks = DrinksMade.objects.filter(user=user.username).order_by('-id')[:5]
        
    context = {
        'member': user_profile,
        'motivational_msg': latest_post,
        
        
        'drinks': user_drinks,
        
    }
    
    print()
    
    if request.method == 'POST':

        user_profile.boozy = request.POST.get('strength')
        user_profile.taste = request.POST.get('taste')
        
         # Get the list of selected spirits and join them into a single string
        selected_spirits = request.POST.getlist('spirit')
        user_profile.spirits = ', '.join(selected_spirits)  # This saves the spirits as a comma-separated string
        
        # Save the data correctly
        user_profile.save()
        
        return redirect('cocktails')
    
   
    return render(request, 'bar_pedro/profile.html', context)

@login_required
def cocktails(request):
    """This function is to run the drinks list match the user preferences and randomly suggest a cocktail"""
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    latest_post =  user_profile.latest_post
    boozy = user_profile.boozy
    taste = user_profile.taste
    spirits = user_profile.spirits
    spirits_list = [spirit.strip() for spirit in spirits.split(',')]
    spirits_pattern = "|".join(spirits_list)
   
    #match the drinks based on preferences
    
    match1 = Drinks.objects.filter(boozy=boozy, taste=taste)
    match2 = match1.filter(spirits__regex=rf'\b({spirits_pattern})\b').values()
    print(match2)
    
    # Check if a cocktail suggestion is already stored in the session
    if 'selected_cocktail' in request.session:
        cocktail_suggestion = request.session['selected_cocktail']
    else:
        cocktail_suggestion = random.choice(list(match2))
        request.session['selected_cocktail'] = cocktail_suggestion  # Store in session
    
    context = {
        'member': user_profile,
        'motivational_msg': latest_post,
        'cocktails': cocktail_suggestion,     
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        #if the user is not satisfied with the suggestion, click and new random cocktail will be shown
        if action == "DMU":
        
            cocktail_suggestion = random.choice(list(match2))
            request.session['selected_cocktail'] = cocktail_suggestion
            context['cocktails'] = cocktail_suggestion
            
        if action == "YES":
            username = user.username
            # Retrieve the cocktail from the session to ensure consistency
            cocktail = request.session.get('selected_cocktail').get("cocktail")
            drink = Drinks.objects.get(cocktail=cocktail)
            rate = request.POST.get('rate')
            comment = request.POST.get('comment')
        
            DrinksMade.objects.create(user=username, cocktail=cocktail, rate=rate, comment=comment, drink=drink)
            
            # Update latest post with a random message
            user_profile.latest_post = random.choice(get_file_content_as_list(RESPONSE_FILE))
            user_profile.save()
            
            # Clear the selected cocktail from the session after saving
            del request.session['selected_cocktail']
            
            return redirect("profile")       
        
        return render(request, 'bar_pedro/cocktails.html', context)

    return render(request, 'bar_pedro/cocktails.html', context)

@login_required
def menu(request):
    """Display the list of all cocktails"""
    cocktails_list = Drinks.objects.all()
    context = { "menu": cocktails_list,
    }
    return render(request, "bar_pedro/menu.html", context)

@login_required
def cocktail_info(request, id):
    "display all the specific cocktail information, clicked on the cocktails list page or my cocktails list"
    cocktail = Drinks.objects.get(id=id)
    context = {
        'cocktail': cocktail
    }
    
    return render(request, "bar_pedro/cocktail_info.html", context)

class LandingPage(TemplateView):
    template_name = "bar_pedro/landing_page.html"

class ImprintView(TemplateView):
    template_name = "bar_pedro/imprint.html"

class PrivacyPolicyView(TemplateView):
    template_name = "bar_pedro/privacy_policy.html"

