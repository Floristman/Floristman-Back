from django.db import models

<<<<<<< HEAD

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    img = models.ImageField()

    def __str__(self):
        return f"{self.name}"

    def result(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "img": self.img
        }


class Products(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField()
    skidka = models.IntegerField(default=False)
    narx = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

    def result(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "skidka": self.skidka,
            "narx": self.narx,
        }

=======
# Create your models here.


# code
>>>>>>> 259d3e27507aedc09e5de6473e26c996783ba0a8
