from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def login_success(request):
    return render(request, 'simple/loginSuccess.html')


def homepage(request):
    return render(request, 'simple/homepage.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        attempted_user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if attempted_user:

            if attempted_user.is_active:
                login(request, attempted_user)
                with open("test.txt", 'a+', encoding='utf-8') as f:
                    f.write("\n")
                    f.write('login success  ' + 'Username:- ' + str(attempted_user.username))
                return redirect('simple:loginsucess')
            else:
                with open("test.txt", 'a+', encoding='utf-8') as f:
                    f.write("\n")
                    f.write('login locked  ' + "Username:- " + str(attempted_user.username))
                return redirect('simple:userlocked')

        else:
            if User.objects.filter(username=request.POST['username']):
                user_exists = User.objects.filter(username=request.POST['username'])
                with open("test.txt", 'a+', encoding='utf-8') as f:
                    f.write("\n")
                    f.write('login failed  ' + "Username:- " + str(user_exists[0]))

                if user_exists:
                    user_invalid_atttempts = f'incorrect_{request.POST["username"]}'

                    if user_invalid_atttempts in request.session:
                        request.session[user_invalid_atttempts] += 1

                        with open("test.txt", 'a+', encoding='utf-8') as f:
                            f.write("\n")
                            f.write(
                                'login attempt no:- ' + str(
                                    request.session[user_invalid_atttempts]) + " Username:- " + str(user_exists[0]))

                        if request.session[user_invalid_atttempts] == 3:
                            send_mail('ACCOUNT LOCKED',
                                      '*** Your account has been locked.This is an automatically generated email, please do not reply ...',
                                      settings.EMAIL_HOST_USER,
                                      [user_exists[0].email], fail_silently=False)

                            user_exists[0].is_active = False
                            user_exists[0].save()
                            request.session.pop(user_invalid_atttempts)
                    else:
                        request.session[user_invalid_atttempts] = 1

    else:
        form = AuthenticationForm()
    return render(request, 'simple/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('simple:login')


def userlocked(request):
    return render(request, 'simple/userlocked.html')
