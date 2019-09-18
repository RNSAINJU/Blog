from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

def login_view(request,link='home'):
    if request.method == 'POST':
        form=LoginForm(request.POST or None)

        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user= authenticate(request,username=username, password=password)
            if user is not None:
                print("User logged in")
                login(request, user)
                return redirect(link)
            else:
                print("Error while logging in")
    else:
        form=LoginForm()

    return render(request,'auth/login.html',{'form': form,})


def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            username=form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            #Create user
            user=User.objects.create_user(username,email,password)
            user.save()


            login(request,user)
            return redirect('home')

    else:
        form=RegistrationForm()
    return render(request,'auth/signup.html',{'form': form,})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model=User
    fields=('username', 'email',)
    template_name= 'auth/my_account.html'
    success_url=reverse_lazy('my_account')

    def get_object(self):
        return self.request.user