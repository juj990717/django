from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'acc/index.html')

def userlogin(request):
    if request.method=="POST":
        un=request.POST.get("name")
        up=request.POST.get("pass")
        u=authenticate(username=un, password=up)
        if u:
            login(request, u) # request에 u 레코드를 실어줌
            messages.success(request, f"{u}!! Welcome!!")
            return redirect("acc:index")
        else:
            messages.error(request,"일치하는 계정이 없습니다.")
    return render(request, "acc/login.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")

def signup(request):
    if request.method=="POST":
        un=request.POST.get("uname")
        up=request.POST.get("upass")
        uc=request.POST.get("ucomm")
        pi=request.FILES.get("upic")
        User.objects.create_user(username=un, password=up, comment=uc, pic=pi)
        return redirect("acc:login")
    return render(request, 'acc/signup.html')

def profile(request):
    return render(request, "acc/profile.html")

def update(request):
    if request.method=="POST":
        u=request.user
        ue=request.POST.get("umail")
        uc=request.POST.get("ucomm")
        pi=request.FILES.get("upic")
        u.email, u.comment = ue, uc
        if pi:
            u.pic.delete()
            u.pic = pi
        u.save()
        messages.info(request, "수정되었습니다.")
        return redirect("acc:profile")
    return render(request, "acc/update.html")

def changepw(request):
    u=request.user
    cp=request.POST.get("cpass")
    if check_password(cp, u.password):
        np=request.POST.get("npass")
        u.set_password(np)
        u.save()
        messages.info(request, "패스워드가 변경되었습니다. 다시 로그인 해주세요")
        return redirect("acc:login")
    else:
        messages.error(request, "입력하신 비밀번호와 새로운 비밀번호가 일치하지 않습니다.")
    return redirect("acc:update")

def ckpw(request):
    u=request.user
    ck=request.POST.get("ck")
    if check_password(ck, u.password):
        u.pic.delete()
        u.delete()
        messages.success(request, "계정이 삭제되었습니다.")
        return redirect("acc:index")
    else:
        messages.error(request, "입력하신 비밀번호가 일치하지 않습니다.")
    return redirect("acc:profile")