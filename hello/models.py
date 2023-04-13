from django.db import models
from django.utils import timezone
from pathlib import Path
from django.core.files import File
from PIL import Image
import os

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

#--------------------- Multi-Pic-Handling ---------------------------------------

class AllCats(models.Model): # erlaubte Kategorien für Bildserien
    cat = models.CharField(max_length=80, db_index=True, unique=True)
    description = models.TextField()

class PicSeries(models.Model): # 1 ...n shots, die zusammengehören
    title = models.CharField(max_length=80)
    dateCreated = models.DateTimeField()
    dateCaptured = models.DateTimeField()
    dateModified = models.DateTimeField()
    owner = models.CharField(max_length=80)
    description = models.TextField()
    heroIdBigPic = models.BigIntegerField("ID from Hero-BigPic")
    heroIdThumbnail = models.BigIntegerField("ID from Hero-Thumbnail")
    catPrime = models.ForeignKey(AllCats, on_delete=models.CASCADE) # Primäre Kategorie der Bildserie

class SeriesCats(models.Model): # Alle Kategorien einer Serie
    cat = models.ForeignKey(AllCats, on_delete=models.CASCADE)
    series = models.ForeignKey(PicSeries, on_delete=models.CASCADE)

class SinglePic(models.Model):
    series = models.ForeignKey(PicSeries, on_delete=models.CASCADE)
    bigPic = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='images/thumbnails')

#------------------ /Multi-Pic-Handling ------------------------------------------

class Post(models.Model):
    title = models.TextField()
    owner = models.TextField(default="unknown")
    log_date = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(default='images/thumbnails/no_thumbnail.jpg', upload_to='images/thumbnails')


    def __str__(self):
        return self.title

    def create_thumbnail(self):
        if self.id:
            try:
                img_path_p, img_path_f = os.path.split(self.cover.path)
                thn_path_p, thn_path_f = os.path.split(self.thumbnail.path)
            except:
                thn_path_f="no_thumbnail.jpg"
                thn_path_p="/root/tutorial/media/images/thumbnails"
#            if img_path_f == thn_path_f:
#                return self.thumbnail.path # Thumnail existiert schon
            else:
                # Create thumbnail as Image-Object
                img_thumbnail = Image.open(self.cover)
                img_thumbnail.thumbnail((256,256))
                # Save thumbnail as File
                thn_path = thn_path_p + "/" + img_path_f
                if os.path.exists(thn_path):
                    os.remove(thn_path)
                img_thumbnail.save(thn_path)
                thn_path_model = "/images/thumbnails/" + img_path_f
                self.thumbnail=thn_path_model
                self.save()
                return
        else:
            return 