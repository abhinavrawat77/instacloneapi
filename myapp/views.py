
from django.shortcuts import render, redirect
from forms import SignUpForm,LoginForm
from models import UserModel
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print 'Sign up form submitted'
        return render(request, 'success.html')
    elif request.method == 'GET':
        form = SignUpForm()
    return render(request, 'index.html', {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                # Check for the password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response

                else:
                    print 'User is invalid'

    elif request.method == "GET":
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def feed_view(request):
    return render(request, 'feed.html')

def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None