from django.db import models

class Heading(models.Model):
    title = models.CharField(max_length=255)
    underline = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Card(models.Model):
    heading = models.ForeignKey(Heading, related_name="cards", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cards/images/')
    card_color = models.CharField(max_length=7, default='#ffffff')  # Hex color code

    def __str__(self):
        return self.name
