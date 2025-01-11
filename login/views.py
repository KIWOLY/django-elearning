from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile, Note, Feedback, PasswordReset, Subject, Number
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseForbidden, FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.utils import timezone  






def sinup(request):
    if request.method == 'POST':
        # Getting input data from form
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        category = request.POST.get('category')
        registration_number = request.POST.get('registration_number')

        # Check if all fields are filled
        if not all([firstname, lastname, username, email, phone, password, password2, category, registration_number]):
            messages.info(request, 'All fields are required.')
            return redirect('sinup')

        # Check if the registration number is valid and exists in the Number model
        try:
            number_instance = Number.objects.get(number=registration_number)
        except Number.DoesNotExist:
            messages.info(request, 'Your registration number shows that you are not a member of ISM 2 .')
            return redirect('sinup')

        # Ensure the registration number is not used by any other profile
        if Profile.objects.filter(registration_number=number_instance).exists():
            messages.info(request, 'This registration number has already been used.')
            return redirect('sinup')

        # Ensure passwords match
        if password==password2:
            if len(password)<6:
                messages.info(request, 'Password must be at least 6 characters')
                return redirect('sinup')    

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('sinup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('sinup')
            else:
                user=User.objects.create_user(username=username, password=password, email=email)
                user.is_active = False
                user.first_name = firstname
                user.last_name = lastname
                user.is_active = False
                user.save()

                profile = Profile.objects.get(user=user)
                profile.phone = phone
                profile.category = category
                profile.registration_number = registration_number
                profile.save()
                
                # number_instance.delete()

            # Send the email verification link
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_link = request.build_absolute_uri(f"/verify-email/{uid}/{token}/")
                send_mail(
                    'Verify Your Email Address',
                    f'Click the link to verify your email: {verification_link}',
                    'admin@example.com',
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Account created successfully. Check your email to verify your account.')
                return redirect('login')
        
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('sinup')       
    return render( request, 'sinup.html')    
            
        


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect('login')
    else:
        return HttpResponse("Verification link is invalid or expired.")
    return redirect('signup')


@login_required
def profile_view(request):
    # Fetch the profile of the currently logged-in user
    profile = request.user.profile  
    return render(request, 'profile.html', {'profile': profile})


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
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    subjects = Subject.objects.all()  # Fetch all subjects
    return render(request, 'dashboard.html',{'subjects': subjects})



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
            return render(request, 'feedback.html')

@login_required
def upload(request):
    # Check if the user is a Lecturer
    if request.user.profile.category != 'Lecturer':
        messages.error(request, 'You do not have permission to upload notes.')
        return redirect('dashboard')

    # Handle the POST request
    if request.method == 'POST':
        uploaded_file = request.FILES.get('noteFile')
        title = request.POST.get('title')
        subject_name = request.POST.get('subject')  # Extract the subject from the form

        # Validate that all fields are provided
        if not uploaded_file or not title or not subject_name:
            messages.error(request, 'All fields are required.')
            return redirect('upload')
        
        # Retrieve the Subject instance
        subject = get_object_or_404(Subject, name=subject_name)

        # Create a new Note instance and save it to the database
        note = Note.objects.create(
            lecturer=request.user,
            title=title,
            subject=subject,  # Save the subject
            file=uploaded_file
        )
        messages.success(request, 'Note uploaded successfully.')
        return redirect('dashboard')

    # If not a POST request, redirect or render a page
    messages.error(request, 'Invalid request method.')
    return redirect('upload')




@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    # Optional: Restrict deletion to the note owner or admin
    if request.user != note.lecturer and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete this note.")
    
    note.delete()
    return redirect('dashboard')  # Replace 'dashboard' with your desired redirect URL



def note_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    notes = subject.notes.all()
    return render(request, 'notes_list.html', {'subject': subject, 'notes': notes})

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})



def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    try:
        return FileResponse(note.file.open(), as_attachment=True)
    except FileNotFoundError:
        raise Http404("File not found")



def forgot_password(request):
    if request.method == 'POST':
        email=request.POST.get('email')

        try:
            user=User.objects.get(email=email)
            new_password_reset=PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url=reverse('reset_password',kwargs={'reset_id':new_password_reset.reset_id})
            full_password_reset_url=f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body=f'hello {user.username}, please reset your password using the link below: \n\n\n{full_password_reset_url}'
            
            email_message=EmailMessage(
                'Reset your password',    
                email_body,
                settings.EMAIL_HOST_USER,
                [email],          

            )
            email_message.fail_silently=True
            email_message.send()

            return redirect('password_reset_sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.info(request, f'No user with email {email} found.')
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')

def password_reset_sent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
       return render(request, 'password_reset_sent.html')
    
    else:
        messages.info(request,"invalid reset iD")
        return redirect('forgot_password')




def reset_password(request,reset_id):
    try:
        password_reset_id=PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password=request.POST.get('password')
            confirm_password=request.POST.get('confirm_password')

            password_have_error=False

            if password!=confirm_password:
                password_have_error=True
                messages.info(request, 'Passwords do not match')

            if len(password)<6:
                password_have_error=True
                messages.info(request, 'Password must be at least 6 characters')

            expiration_time=password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                password_have_error=True
                messages.info(request, 'Password reset link has expired')
                password_reset_id.delete()

            if not password_have_error:
                user=password_reset_id.user
                user.set_password(password)
                user.save()
                password_reset_id.delete()

                messages.success(request, 'Password reset successfully')
                return redirect('login')
            else:
                return redirect('reset_password', reset_id=reset_id)
                
    except PasswordReset.DoesNotExist:
        messages.info(request, "invalid reset id")
        return redirect('forgot_password')

    return render(request, 'reset_password.html')



def page_not_found(request, exception):
    return render(request, '404.html')
