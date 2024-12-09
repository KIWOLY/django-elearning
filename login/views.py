from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile ,Note ,Feedback,PasswordReset,Student
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator





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
                    profile = Profile.objects.create(user=user, phone=phone, category=category)
                    profile.phone = phone
                    profile.category = category
                    user.is_active = False
                    # Save the user
                    user.save()
                    profile.save()

                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                # verification_link = request.build_absolute_uri(reverse('verify_email', args=[uid, token]))
                    verification_link = request.build_absolute_uri(f"/verify-email/{uid}/{token}/")
                    send_mail(
                    'Verify Your Email Address',
                     f'Click the link to verify your email: {verification_link}',
                    'admin@example.com',
                    [email],)
                    fail_silently=False,

                    messages.info(request,"Check your email to verify your account.")
                    return redirect('sinup')
                    # Create a profile associated with the user
                    


                    # Optionally, set additional fields directly on the Profile object
                    
                    

                    messages.success(request, 'Account created successfully.')
                    return redirect('login')
                except ValidationError as e:
                    messages.error(request, e.message)
                    return redirect('sinup')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('sinup')

    else:
        return render(request, 'sinup.html')


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
    return render(request, 'dashboard.html')



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
    return render(request, 'note_list.html', {'notes': notes})



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
    