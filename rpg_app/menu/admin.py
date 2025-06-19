from django.contrib import admin
from .models import Account, ItemData, Monster, Character, Items, Setting

admin.site.register(ItemData)
admin.site.register(Monster)

admin.site.register(Account)
admin.site.register(Character)
admin.site.register(Items)
admin.site.register(Setting)
