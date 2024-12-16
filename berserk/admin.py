from django.contrib import admin

from berserk.models import BerserkCharacter, BerserkCreature, BerserkGeography, BerserkArmy, BerserkArtifact, Album


@admin.register(BerserkCharacter)
class BerserkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'jap_name', 'eng_name', 'creature', 'qoute', 'description', 'army', 'picture', 'user']

@admin.register(BerserkCreature)
class BerserkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']

@admin.register(BerserkGeography)
class BerserkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']

@admin.register(BerserkArmy)
class BerserkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','description', 'geography']

@admin.register(BerserkArtifact)
class BerserkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'owner', 'harm_to', 'inventor', 'picture']    

@admin.register(Album)
class BerserkAdmin(admin.ModelAdmin):
    list_display = ['id', 'creature', 'picture']        
