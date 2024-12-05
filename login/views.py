from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile ,Note ,Feedback
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views





def sinup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        category = request.POST['category']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('sinup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('sinup')
            else:
                try:
                    # Create a new user
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # Set first name and last name
                    user.first_name = firstname
                    user.last_name = lastname
                    # Save the user
                    user.save()
                    # Create a profile associated with the user
                    profile = Profile.objects.create(user=user, phone=phone, category=category)


                    # Optionally, set additional fields directly on the Profile object
                    profile.phone = phone
                    profile.category = category
                    profile.save()

                    messages.success(request, 'Account created successfully.')
                    return redirect('login')
                except ValidationError as e:
                    messages.error(request, e.message)
                    return redirect('sinup')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('sinup')

    else:
        return render(request, 'login/sinup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')
    else:
        return render(request, 'login/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def home(request):
    return render(request, 'login/home.html')

def password_reset(request):
    if request.method == 'POST':
        # If the form is submitted, Django's PasswordResetView will handle the process
        return auth_views.PasswordResetView.as_view(
            template_name='login/password_reset.html'
        )(request)
    else:
        # If it's a GET request, simply render the password reset form
        return render(request, 'login/password_reset.html')

def dashboard(request):
    return render(request, 'login/dashboard.html')



def feedback(request):
     if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            feedback_content = request.POST.get('feedback')

            # Create and save the feedback object
            feedback = Feedback(name=name, email=email, feedback=feedback_content)
            feedback.save()

            # Redirect to a thank you page or any other page
            return redirect('dashboard')  # Adjust the URL as needed
     else:
            return render(request, 'login/feedback.html')

@login_required
def upload(request):
    if request.user.profile.category != 'Lecturer':
        messages.error(request, 'You do not have permission to upload notes.')
        return redirect('dashboard')

    if request.method == 'POST':
        uploaded_file = request.FILES['noteFile']
        title = request.POST['title']  # Assuming you have a 'title' field in your HTML form

        # Create a new Note instance and save it to the database
        note = Note.objects.create(lecturer=request.user, title=title, file=uploaded_file)
        messages.success(request, 'Note uploaded successfully.')
        return redirect('dashboard')

    # return render(request, 'upload.html')



def note_list(request):
    notes = Note.objects.all()
    return render(request, 'login/note_list.html', {'notes': notes})

