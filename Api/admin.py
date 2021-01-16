from django.contrib import admin
from .models import Patient, Doctor, Food, Advice, Chat, SugarLevel, Account, Cooperate, RejectCooperate

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Food)
admin.site.register(Advice)
admin.site.register(Chat)
admin.site.register(SugarLevel)
admin.site.register(Account)
admin.site.register(Cooperate)
admin.site.register(RejectCooperate)
