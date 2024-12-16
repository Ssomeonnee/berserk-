from django.test import TestCase
from rest_framework.test import APIClient

from berserk.models import BerserkCharacter, BerserkCreature, BerserkArmy, BerserkArtifact, BerserkGeography
# Create your tests here.
from model_bakery import baker

class BerserkCreatureViewSetTestCase(TestCase):
   
    def setUp(self):
        self.client = APIClient()
       
    def test_get_list(self):
        creature = baker.make("BerserkCreature")
        r = self.client.get('/api/berserk_creatures/')
        data = r.json()
        print(data)
        
        assert creature.name == data[0]['name']
        assert creature.id == data[0]['id']
        assert len(data) == 1

    def test_create_creature(self):
        
        r = self.client.post("/api/berserk_creatures/",
                             {"name": "Существо",
                              "description": "Описание существа"})
       
        new_creature_id = r.json()['id']

        creatures = BerserkCreature.objects.all()
        assert len(creatures) == 1

        new_creature = BerserkCreature.objects.filter(id=new_creature_id).first()
        assert new_creature.name == "Существо"
        assert new_creature.description == "Описание существа"

    
    def test_delete_creature(self):
        
        creatures = baker.make("BerserkCreature", 10)

        r = self.client.get("/api/berserk_creatures/")
        data = r.json()
        assert len(data) == 10

        creature_id_to_delete = creatures[3].id
        self.client.delete(f'/api/berserk_creatures/{creature_id_to_delete }/')

        r = self.client.get("/api/berserk_creatures/")
        data = r.json()
        assert len(data) == 9

        assert creature_id_to_delete not in [i['id'] for i in data]


    def test_update_creature(self):
        
        creatures = baker.make("BerserkCreature", 10)
        creature: BerserkCreature = creatures[2]

        r = self.client.get(f"/api/berserk_creatures/{creature.id}/")
        data = r.json()
        assert data['name'] == creature.name

        r = self.client.put(f"/api/berserk_creatures/{creature.id}/",
                            {
                                "name": "Существо",
                                "description": "Описание существа"
                            })
        
        assert r.status_code == 200

        r = self.client.get(f"/api/berserk_creatures/{creature.id}/")
        data = r.json()
        assert data['name'] == "Существо"

        creature.refresh_from_db()
        assert data['name'] == creature.name
  

class BerserkCharacterViewSetTestCase(TestCase):
   
    def setUp(self):
        self.client = APIClient()
       
    def test_get_list(self):
        crt = baker.make("BerserkCreature")
        character = baker.make("BerserkCharacter", creature = crt)

        r = self.client.get('/api/berserk_characters/')
        data = r.json()
        print(data)
        
        assert character.name == data[0]['name']
        assert character.id == data[0]['id']
        assert len(data) == 1

    def test_create_character(self):
        
        crt = baker.make("BerserkCreature")
        arm = baker.make("BerserkArmy")

        r = self.client.post("/api/berserk_characters/",
                             {"name": "Персонаж",
                              "jap_name" : "с",
                              "eng_name" : "с",
                              "qoute" : "с", 
                              "description": "Описание персонажа",
                              "creature": crt.id,
                              "army" : arm.id 
                              })
       
        new_character_id = r.json()['id']

        characters = BerserkCharacter.objects.all()
        assert len(characters) == 1

        new_character = BerserkCharacter.objects.filter(id=new_character_id).first()
        assert new_character.name == "Персонаж"
        assert new_character.jap_name == "с"
        assert new_character.eng_name == "с"
        assert new_character.qoute == "с"
        assert new_character.description == "Описание персонажа"
        assert new_character.creature == crt
        assert new_character.army == arm

        
    def test_delete_character(self):
        
        characters = baker.make("BerserkCharacter", 10)

        r = self.client.get("/api/berserk_characters/")
        data = r.json()
        assert len(data) == 10

        character_id_to_delete = characters[3].id
        self.client.delete(f'/api/berserk_characters/{character_id_to_delete }/')

        r = self.client.get("/api/berserk_characters/")
        data = r.json()
        assert len(data) == 9

        assert character_id_to_delete not in [i['id'] for i in data]


    def test_update_character(self): ###############################
        
        characters = baker.make("BerserkCharacter", 10)
        character: BerserkCharacter = characters[2]

        crt = baker.make("BerserkCreature")
        arm = baker.make("BerserkArmy")

        r = self.client.get(f"/api/berserk_characters/{character.id}/")
        data = r.json()
        assert data['name'] == character.name
        assert data['jap_name'] == character.jap_name
        assert data['eng_name'] == character.eng_name
        assert data['qoute'] == character.qoute
        assert data['description'] == character.description
        assert data['creature'] == character.creature
        assert data['army'] == character.army 

        r = self.client.put(f"/api/berserk_characters/{character.id}/",
                            {
                              "name": "Персонаж",
                              "jap_name" : "с",
                              "eng_name" : "с",
                              "qoute" : "с", 
                              "description": "Описание персонажа",
                              "creature": crt.id,
                              "army" : arm.id 
                            })
        
        assert r.status_code == 200

        r = self.client.get(f"/api/berserk_characters/{character.id}/")
        data = r.json()
        print(data)
        assert data['name'] == "Персонаж"
        assert data['jap_name'] == "с"
        assert data['eng_name'] == "с"
        assert data['qoute'] == "с"
        assert data['description'] == "Описание персонажа"
        assert data['creature']['id'] == crt.id
        assert data['army']['id'] == arm.id 

        character.refresh_from_db()
        assert data['name'] == character.name
        assert data['jap_name'] == character.jap_name
        assert data['eng_name'] == character.eng_name
        assert data['qoute'] == character.qoute
        assert data['description'] == character.description
        assert data['creature']['id'] == character.creature.id
        assert data['army']['id'] == character.army.id

class BerserkGeographyViewSetTestCase(TestCase):
   
    def setUp(self):
        self.client = APIClient()
       
    def test_get_list(self):
       
        geography = baker.make("BerserkGeography")

        r = self.client.get('/api/berserk_geography/')
        data = r.json()
        print(data)
        
        assert geography.name == data[0]['name']
        assert geography.id == data[0]['id']
        assert len(data) == 1

    def test_create_geography(self):
        
        r = self.client.post("/api/berserk_geography/",
                             {"name": "Местность",
                              "description": "Описание местности",
                              })
       
        new_geography_id = r.json()['id']

        geography = BerserkGeography.objects.all()
        assert len(geography) == 1

        new_geography = BerserkGeography.objects.filter(id=new_geography_id).first()
        assert new_geography.name == "Местность"
        assert new_geography.description == "Описание местности"

    
    def test_delete_geography(self):
        
        geography = baker.make("BerserkGeography", 10)

        r = self.client.get("/api/berserk_geography/")
        data = r.json()
        assert len(data) == 10

        geography_id_to_delete = geography[3].id
        self.client.delete(f'/api/berserk_geography/{geography_id_to_delete }/')

        r = self.client.get("/api/berserk_geography/")
        data = r.json()
        assert len(data) == 9

        assert geography_id_to_delete not in [i['id'] for i in data]


    def test_update_geography(self): #########################333
        
        geography = baker.make("BerserkGeography", 10)
        geography1: BerserkGeography = geography[2]

        r = self.client.get(f"/api/berserk_geography/{geography1.id}/")
        data = r.json()
        assert data['name'] == geography1.name

        r = self.client.put(f"/api/berserk_geography/{geography1.id}/",
                            {
                                "name": "География",
                            })
        
        #assert r.status_code == 200

        r = self.client.get(f"/api/berserk_geography/{geography1.id}/")
        data = r.json()
        assert data['name'] == "География"

        geography1.refresh_from_db()
        assert data['name'] == geography1.name

class BerserkArmyViewSetTestCase(TestCase):
   
    def setUp(self):
        self.client = APIClient()
       
    def test_get_list(self):
       
        army = baker.make("BerserkArmy")

        r = self.client.get('/api/berserk_army/')
        data = r.json()
        print(data)
        
        assert army.name == data[0]['name']
        assert army.id == data[0]['id']
        assert len(data) == 1

    def test_create_army(self): ####################333
        
        geo = baker.make("BerserkGeography")

        r = self.client.post("/api/berserk_army/",
                             {"name": "Армия",
                              "description": "Описание армии",
                              "geography": ""
                              })
       
        new_army_id = r.json()['id']

        army = BerserkArmy.objects.all()
        assert len(army) == 1

        new_army = BerserkArmy.objects.filter(id=new_army_id).first()
        assert new_army.name == "Армия"
        assert new_army.description == "Описание армии"
        assert new_army.geography == geo


    def test_delete_geography(self):
        
        army = baker.make("BerserkArmy", 10)

        r = self.client.get("/api/berserk_army/")
        data = r.json()
        assert len(data) == 10

        army_id_to_delete = army[3].id
        self.client.delete(f'/api/berserk_army/{army_id_to_delete }/')

        r = self.client.get("/api/berserk_army/")
        data = r.json()
        assert len(data) == 9

        assert army_id_to_delete not in [i['id'] for i in data]


    def test_update_geography(self): ####################3333
        
       army = baker.make("BerserkArmy", 10)

class BerserkArtifactViewSetTestCase(TestCase):
   
    def setUp(self):
        self.client = APIClient()
       
    def test_get_list(self):
       
        artifact = baker.make("BerserkArtifact")

        r = self.client.get('/api/berserk_artifact/')
        data = r.json()
        print(data)
        
        assert artifact.name == data[0]['name']
        assert artifact.id == data[0]['id']
        assert len(data) == 1

    def test_create_artifact(self): #####################################
        
        own = baker.make("BerserkCharacter")
        hrm = baker.make("BerserkCharacter")
        inv = baker.make("BerserkCharacter")

        r = self.client.post("/api/berserk_artifact/",
                             {"name": "Армия",
                              "description": "Описание армии",
                              "owner": own.id,
                              "harm_to": hrm.id,
                              "inventor": inv.id
                              })
       
        new_artifact_id = r.json()['id']

        artifact = BerserkArtifact.objects.all()
        assert len(artifact) == 1

        new_artifact = BerserkArtifact.objects.filter(id=new_artifact_id).first()
        assert new_artifact.name == "Армия"
        assert new_artifact.description == "Описание армии"
        assert new_artifact.owner.id == own.id
        assert new_artifact.harm_to == hrm
        assert new_artifact.inventor == inv


    def test_delete_artifact(self):
        
        artifact = baker.make("BerserkArtifact", 10)

        r = self.client.get("/api/berserk_artifact/")
        data = r.json()
        assert len(data) == 10

        artifact_id_to_delete = artifact[3].id
        self.client.delete(f'/api/berserk_artifact/{artifact_id_to_delete }/')

        r = self.client.get("/api/berserk_artifact/")
        data = r.json()
        assert len(data) == 9

        assert artifact_id_to_delete not in [i['id'] for i in data]


    def test_update_geography(self): ########################
        
       army = baker.make("BerserkArmy", 10)
