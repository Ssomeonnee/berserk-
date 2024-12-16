from django.db import models

# Create your models here.

#class Group(models.Model):
   # name = models.TextField("Название")

   # class Meta:
   #     verbose_name="Принадлежность"
   #     verbose_name_plural="Принадлежности"

   # def __str__(self) -> str:
   #     return self.name    

#class Berserk(models.Model):
    #name = models.TextField("Имя")
    #group_name = models.TextField("Класс")
    #group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)

    #class Meta:
    #    verbose_name="Персонаж берсерка"
    #    verbose_name_plural="Персонажи берсерка"

    #def __str__(self) -> str:
    #    return self.name        


class BerserkCharacter(models.Model):
    name = models.TextField("Имя")
    jap_name = models.TextField("Японское имя")
    eng_name = models.TextField("Английское имя")
    creature = models.ForeignKey("BerserkCreature", on_delete=models.CASCADE, null=True)
    qoute = models.TextField("Цитата")
    description = models.TextField("Описание")
    army = models.ForeignKey("BerserkArmy", on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField("Изображение", null=True, blank=True, upload_to="berserkCharacters")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Персонаж берсерка"
        verbose_name_plural="Персонажи берсерка"

    def __str__(self) -> str:
        return self.name        

class BerserkCreature(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
   
    class Meta:
        verbose_name="Существо"
        verbose_name_plural="Существа"

    def __str__(self) -> str:
        return self.name        

class BerserkGeography(models.Model):
    name = models.TextField("Наименование")
    description = models.TextField("Описание")

    class Meta:
        verbose_name="Местность"
        verbose_name_plural="Местности"

    def __str__(self) -> str:
        return self.name        

class BerserkArmy(models.Model):
    name = models.TextField("Наименование")
    description = models.TextField("Описание")
    geography = models.ForeignKey("BerserkGeography", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Армия"
        verbose_name_plural="Армии"

    def __str__(self) -> str:
        return self.name        

class BerserkArtifact(models.Model):
    name = models.TextField("Наименование")
    description = models.TextField("Описание")
    owner = models.ForeignKey("BerserkCharacter", on_delete=models.CASCADE, null=True,
        related_name='artifacts_owner')
    harm_to = models.ForeignKey("BerserkCreature", on_delete=models.CASCADE, null=True,
        related_name='artifacts_harm_to')
    inventor = models.ForeignKey("BerserkCharacter", on_delete=models.CASCADE, null=True,
        related_name='artifacts_inventor')
    picture = models.ImageField("Изображение", null=True, upload_to="berserkArtifact")

    class Meta:
        verbose_name="Артефакт"
        verbose_name_plural="Артефакты"

    def __str__(self) -> str:
        return self.name                
    
class Album(models.Model):
    creature = models.ForeignKey("BerserkCreature", on_delete=models.CASCADE,
        related_name='photo_creature', default="0")
    picture = models.ImageField("Изображение", upload_to="Album")

    class Meta:
        verbose_name="Альбом"
        verbose_name_plural="Альбомы"

    def __str__(self) -> str:
        return "Альбом"                 