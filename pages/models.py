from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, default='david@email.com')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse("Article_detail", kwargs={"pk": self.pk})
