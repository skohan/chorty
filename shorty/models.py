from django.db import models
import django.contrib.auth.models as auth_models



class Profile(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete= models.CASCADE) 
    is_premium = models.BooleanField(default=False)
    no_of_urls = models.IntegerField(default=0)
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return f"{self.user} | {self.is_premium}"



class Url(models.Model):
    slug = models.SlugField(max_length=100)
    url = models.URLField()
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.slug} - {self.url}"

    
    
