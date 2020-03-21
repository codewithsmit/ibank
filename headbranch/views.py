from django.shortcuts import HttpResponse, render, redirect
from . models import HeadBranch, Branch, HeadBranch_Transaction, Branch_Transaction

# Create your views here.

def hb_auth(request):
    params = {}
    if request.session.get('hb_auth',False):
        params['hb_auth'] = True
        hbranch =  HeadBranch.objects.all()
        params['balance'] = hbranch[0].hbranch_balance
    else:
        params['hb_auth'] = False
    return params

def alert(request,params):
    if request.session.get('alert',False):
        params['alert'] = request.session.get('alert')
        request.session.pop('alert')
    return params

def index(request):
    params = hb_auth(request)
    params = alert(request,params)
    if params['hb_auth'] == True:
        branchs = Branch.objects.all()
        bbalance = 0
        bcount = len(branchs)
        for i in branchs:
            bbalance += i.branch_balance
        total = bbalance + params['balance']
        params['bbalance'] = bbalance
        params['bcount'] = bcount
        params['total'] = total
    params['page'] = 'index'
    return render(request,'headbranch/index.html',params)

def branch(request):
    print(request)
    params = hb_auth(request)
    if params['hb_auth'] == False:
        return redirect('/headbranch')
    params = alert(request,params)
    if params['hb_auth'] == True:
        branchs = Branch.objects.all()
        params['branchs'] = branchs
    params['page'] = 'branch'
    return render(request,'headbranch/branch.html',params)

def account(request):
    params = hb_auth(request)
    if params['hb_auth'] == False:
        return redirect('/headbranch')
    params = alert(request,params)
    params['page'] = 'account'
    return render(request,'headbranch/account.html',params)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        hbranch = HeadBranch.objects.filter(hbranch_username = username)
        if hbranch.exists():
            if hbranch[0].hbranch_password == password:
                request.session['hb_auth'] = True
                request.session['alert'] = "Head Branch Login Successfully"
            else:
                request.session['alert'] = "Invalid Login Password"
        else:
            request.session['alert'] = "Invalid Username or Password"
    return redirect('/headbranch')

def logout(request):
    request.session['hb_auth'] = False
    return redirect('/headbranch')

def Send_Money(branch,amount):
    HeadBranch_Transaction.objects.create(hbranch_tra_branch = branch, hbranch_tra_type = 0, hbranch_tra_amount = amount)
    Branch_Transaction.objects.create(branch_tra_with = 'branch', branch_tra_branch=branch, branch_tra_account = 0, branch_tra_type = 1, branch_tra_amount = amount)
    branch = Branch.objects.get(branch_id = branch)
    hbranch = HeadBranch.objects.get(hbranch_id=2)
    branch.branch_balance += amount
    branch.save()
    hbranch.hbranch_balance -= amount 
    hbranch.save()

def Recive_Money(branch,amount):
    HeadBranch_Transaction.objects.create(hbranch_tra_branch = branch, hbranch_tra_type = 1, hbranch_tra_amount = amount)
    Branch_Transaction.objects.create(branch_tra_with = 'branch', branch_tra_branch=branch, branch_tra_account = 0, branch_tra_type = 0, branch_tra_amount = amount)
    branch = Branch.objects.get(branch_id = branch)
    hbranch = HeadBranch.objects.get(hbranch_id=2)
    branch.branch_balance -= amount
    branch.save()
    hbranch.hbranch_balance += amount
    hbranch.save()

def send_money(request):
    params = hb_auth(request)
    if params['hb_auth'] == False:
        return redirect('/headbranch')
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id',0)
        amount = int(request.POST.get('amount',0))
        if branch_id == 0 or amount == 0:
            request.session['alert'] = "Invelid Transaction"
        else:
            branch = Branch.objects.filter(branch_id = branch_id)
            if len(branch) != 0:
                hbranch = HeadBranch.objects.all()
                if hbranch[0].hbranch_balance >= amount:
                    newbal = branch[0].branch_balance+amount
                    request.session['alert'] = "Money Send to "+str(branch[0].branch_name)+", New Balance is "+str(newbal)
                    Send_Money(branch_id,amount)
                else:
                    request.session['alert'] = "insufficient Cash"
    return redirect('/headbranch/branch')

def recive_money(request):
    params = hb_auth(request)
    if params['hb_auth'] == False:
        return redirect('/headbranch')
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id',0)
        amount = int(request.POST.get('amount',0))
        print(branch_id,amount)
        if branch_id == 0 or amount == 0:
            request.session['alert'] = "Invelid Transaction"
        else:
            branch = Branch.objects.filter(branch_id = branch_id)
            if len(branch) != 0:
                hbranch = HeadBranch.objects.all()
                if branch[0].branch_balance >= amount:
                    newbal = branch[0].branch_balance - amount
                    request.session['alert'] = "Money Recived From "+str(branch[0].branch_name)+", New Balance is "+str(newbal)
                    Recive_Money(branch_id,amount)
                else:
                    request.session['alert'] = "insufficient Cash in Branch"
    return redirect('/headbranch/branch')

def add_branch(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        branchs = Branch.objects.filter(branch_username = username)
        if len(branchs) == 0:
            if name == '' or username == '' or password == '':
                request.session['alert'] = "Fill All Details of Branch"
            else:
                Branch.objects.create(branch_name = name, branch_username = username, branch_password = password)
                request.session['alert'] = 'Branch Added Successfully, Name : '+name+', Username : '+username
        else:
            request.session['alert'] = "Branch Username Alredy Assist"
    return redirect('/headbranch/branch')