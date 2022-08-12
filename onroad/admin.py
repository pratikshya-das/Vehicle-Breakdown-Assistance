from django.contrib import admin
from onroad.models import *
from django.contrib.auth import get_user_model

admin.site.register(Business)
admin.site.register(Feedback)
admin.site.register(User)
admin.site.register(UserReg)
admin.site.register(Payment)
admin.site.register(PasswordReset)


