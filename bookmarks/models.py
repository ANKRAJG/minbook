from django.db import models

class Bookmark(models.Model):
    task = models.URLField(max_length=200)
    tag_name = models.TextField()
    
    def __str__(self):
        return self.task

    

    
class Tag_list(models.Model):
    tags = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.tags