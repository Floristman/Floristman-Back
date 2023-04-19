from django.shortcuts import render, redirect


# Create your views here.
def sign_up(requests):
    ctx = {

    }
    return render(requests, 'regis/register.html', ctx)


def sign_in(requests):
    ctx = {

    }
    return render(requests, 'regis/login.html', ctx)


def sign_out(requests):
    return redirect("sign-in")
