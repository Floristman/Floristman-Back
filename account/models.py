from django.db import models

from sayt.models import User


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


class Basket(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if "like" in kwargs and kwargs['like']:
    #         self.like = kwargs['like']
    #      elif 'dislike' in kwargs and kwargs['dislike']:
    #
    #
    #     return super(Likes, self).save(**args, **kwargs)
