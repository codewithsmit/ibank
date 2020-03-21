from django.shortcuts import HttpResponse, render, redirect
from headbranch.models import Branch, Account
# Create your views here.

def b_auth(request):
    params = {}
    if request.session.get('b_auth',False):
        params['b_auth'] = True
        branch =  Branch.objects.filter(branch_id = request.session['b_id'] )
        params['balance'] = branch[0].branch_balance
        params['b_name'] = branch[0].branch_name
        params['b_username'] = branch[0].branch_username
    else:
        params['hb_auth'] = False
    return params

def alert(request,params):
    if request.session.get('alert',False):
        params['alert'] = request.session.get('alert')
        request.session.pop('alert')
    return params

def index(request):
    params = b_auth(request)
    params = alert(request,params)
    params['page'] = 'index'
    return render(request,'branch/index.html',params)

def transaction(request):
    params = b_auth(request)
    params = alert(request,params)
    params['page'] = 'transaction'
    branch = Branch.objects.get(branch_id = request.session.get('b_id'))
    accounts = Account.objects.filter(account_branch_id = branch)
    params['accounts'] = accounts
    return render(request,'branch/transaction.html',params)

def account(request):
    params = b_auth(request)
    params = alert(request,params)
    params['page'] = 'account'
    return render(request,'branch/account.html',params)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        branch = Branch.objects.filter(branch_username = username)
        if branch.exists():
            if branch[0].branch_password == password:
                request.session['b_auth'] = True
                request.session['b_id'] = branch[0].branch_id
                print("Id is set")
                request.session['alert'] = "Branch Login Successfully"
            else:
                request.session['alert'] = "Invalid Login Password"
        else:
            request.session['alert'] = "Invalid Username or Password"
    return redirect('/branch')

def logout(request):
    request.session['b_auth'] = False
    return redirect('/branch')