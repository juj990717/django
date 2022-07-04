from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Board, Reply
from django.contrib import messages
# Create your views here.


def index(request):
    pg = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b=Board.objects.filter(subject__contains=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u=User.objects.get(username=kw)
                b=Board.objects.filter(writer=u)
            except:
                b=Board.objects.none()
            pass
        elif cate == "con":
            b=Board.objects.filter(content__contains=kw)
        else:
            b=Board.objects.none()
    else:
        b=Board.objects.all()


    pag=Paginator(b, 3)
    obj=pag.get_page(pg)
    context={
        'bset' : obj,
        'kw' : kw,
        'cate' : cate
    }
    return render(request, "board/index.html",context)

def detail(request, bpk):
    b=Board.objects.get(id=bpk)
    r=b.reply_set.all()
    context={
        'b' : b,
        'rset' : r
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b=Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else: 
        messages.error(request, "삭제할 수 없습니다. 해킹 계속 시도하신다면 법적 처리하겠습니다.")
    return redirect("board:index")

def create(request):
    if request.method=="POST":
        s=request.POST.get("sub")
        c=request.POST.get("con")
        Board(subject=s, writer=request.user, 
        content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def update(request, bpk):
    b=Board.objects.get(id=bpk)
    if request.user == b.writer:
        if request.method=="POST":
            s=request.POST.get("sub")
            c=request.POST.get("con")
            b.subjecT, b.content=s, c
            b.save()
            return redirect("board:detail", bpk)
    else:
        messages.error(request, "수정할 수 없습니다. 해킹 계속 시도하신다면 법적 처리하겠습니다.")
        return redirect("board:index")
    context={
        'b':b
    }
    return render(request, "board/update.html", context)

def dreply(request, bpk, rpk):
    r=Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
        return redirect("board:detail", bpk)
    else:
        messages.error(request, "댓글을 삭제할 수 없습니다. 해킹 계속 시도하신다면 법적 처리하겠습니다.")
        return redirect("board:detail", bpk)

def creply(request, bpk):
    b=Board.objects.get(id=bpk)
    c=request.POST.get("comm")
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b=Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def unlikey(request, bpk):
    b=Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)