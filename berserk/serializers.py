from rest_framework import serializers
from django.contrib.auth.models import User
from berserk.models import BerserkCharacter, BerserkCreature, BerserkGeography, BerserkArmy, BerserkArtifact, Album

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  
        
class BerserkGeographySerializer(serializers.ModelSerializer):
    class Meta:
        model = BerserkGeography
        fields = ['id', 'name','description']

class BerserkGeographyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BerserkGeography
        fields = ['id', 'name','description']        

class BerserkArmySerializer(serializers.ModelSerializer):
    geography = BerserkGeographySerializer(read_only=True)
    class Meta:
        model = BerserkArmy
        fields = ['id', 'name','description', 'geography']

class BerserkArmyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BerserkArmy
        fields = ['id', 'name','description', 'geography']        

class BerserkCreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BerserkCreature
        fields = ['id', 'name', 'description']   

class BerserkCreatureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BerserkCreature
        fields = ['id', 'name', 'description']   

class AlbumSerializer(serializers.ModelSerializer):
    creature = BerserkCreatureSerializer(read_only=True)
    class Meta:
        model = Album
        fields = ['id', 'creature', 'picture']    

class AlbumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'creature', 'picture'] 

class BerserkCharacterSerializer(serializers.ModelSerializer):
    creature = BerserkCreatureSerializer(read_only=True)
    army = BerserkArmySerializer(read_only=True)

    class Meta:
        model = BerserkCharacter
        fields = ['id', 'name', 'jap_name', 'eng_name', 'creature', 'qoute', 'description', 'army', 'picture', 'user']

class BerserkCharacterCreateSerializer(serializers.ModelSerializer): # создать в админке пользователя который может входить, запретить доступ пользователям которые не авторизованы
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
     
    class Meta:
        model = BerserkCharacter
        fields = ['id', 'name', 'jap_name', 'eng_name', 'creature', 'qoute', 'description', 'army', 'picture', 'user']

class BerserkArtifactSerializer(serializers.ModelSerializer):
    owner = BerserkCharacterSerializer(read_only=True)
    harm_to = BerserkCreatureSerializer(read_only=True)
    inventor = BerserkCreatureSerializer(read_only=True)
    class Meta:
        model = BerserkArtifact
        fields = ['id', 'name',  'description', 'owner', 'harm_to', 'inventor', 'picture']    

class BerserkArtifactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BerserkArtifact
        fields = ['id', 'name', 'description', 'owner', 'harm_to', 'inventor', 'picture']  

                       

     