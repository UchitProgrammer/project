from django.contrib import admin
from .models import User,Course,Questions,Results,Faculty_Subject,Contact
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Questions)
admin.site.register(Results)
admin.site.register(Faculty_Subject)
admin.site.register(Contact)