from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Account
from django.contrib.auth.hashers import make_password,check_password


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Account
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})




def accounts(request):
    users = Account.objects.all()  # fetch all records
    return render(request, 'accounts.html', {'users': users})


def login(request):
    error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Account.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id  # Save login session
                    return render(request,'message.html')
                    # return redirect('accounts', user_id=user.id)
                else:
                    error = "Invalid email or password."
            except Account.DoesNotExist:
                error = "Invalid email or password."
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})

def logout(request):
    request.session.flush()  # Clears all session data
    return redirect('login')
