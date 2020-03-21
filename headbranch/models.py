from django.db import models
from datetime import datetime
# Create your models here.

class HeadBranch(models.Model):
    hbranch_id = models.AutoField(primary_key=True)
    hbranch_username = models.CharField(max_length=50,unique=True)
    hbranch_balance = models.IntegerField(default=0)
    hbranch_password = models.CharField(max_length=100,default='')

    def __str__(self):
        return str(self.hbranch_balance)

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_username = models.CharField(max_length=50,unique=True)
    branch_name = models.CharField(max_length=50)
    branch_balance = models.IntegerField(default=0)
    branch_password = models.CharField(max_length=100,default='')

    def __str__(self):
        return str(self.branch_name)+" : "+str(self.branch_balance)

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE)
    account_username = models.CharField(max_length=50,unique=True)
    account_name = models.CharField(max_length=50)
    account_mobile = models.CharField(max_length=10)
    account_balance = models.IntegerField(default=0)
    account_password = models.CharField(max_length=100,default='')

    def __str__(self):
        return str(self.account_name)+" : "+str(self.account_balance)+" - "+str(self.account_branch_id.branch_name)

class HeadBranch_Transaction(models.Model):
    hbranch_tra_id = models.AutoField(primary_key=True)
    hbranch_tra_branch = models.IntegerField(default=0)
    hbranch_tra_type = models.IntegerField()
    hbranch_tra_amount = models.IntegerField()
    hbranch_tra_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        result = ""
        if self.hbranch_tra_type == 0:
            result+="Send to "
        else:
            result+="Recived From"
        branch = Branch.objects.filter(branch_id = self.hbranch_tra_branch)
        result+=str(branch[0].branch_name)+" - "+str(self.hbranch_tra_amount)
        return result


class Branch_Transaction(models.Model):
    branch_tra_id = models.AutoField(primary_key=True)
    branch_tra_with = models.CharField(max_length=10)
    branch_tra_branch = models.IntegerField(default=0)
    branch_tra_account = models.IntegerField()
    branch_tra_type = models.IntegerField()
    branch_tra_amount = models.IntegerField()
    branch_tra_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        result = ""
        branch = Branch.objects.filter(branch_id = self.branch_tra_branch)
        # result += branch.branch_name+" "
        if self.branch_tra_with == 'branch':
            if self.branch_tra_type == 0:
                result+="Send to Head Branch"
            else:
                result+="Recived From Head Branch"
        else:
            result+="Account"
        result+=" - "+str(self.branch_tra_amount)
        return result

# .objects.all().delete()