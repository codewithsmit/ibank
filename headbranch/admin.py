from django.contrib import admin
from . models import HeadBranch, Branch, Account, HeadBranch_Transaction, Branch_Transaction
# Register your models here.

admin.site.register(HeadBranch)
admin.site.register(Branch)
admin.site.register(Account)
admin.site.register(HeadBranch_Transaction)
admin.site.register(Branch_Transaction)