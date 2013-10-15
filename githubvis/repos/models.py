from django.db import models

# Create your models here.
class Repo(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    

class Actor(models.Model):
    full_name = models.CharField(max_length=255)
    lat = models.FloatField(default = 0)   
    lng = models.FloatField(default = 0)
    loc = models.CharField(max_length = 255, default = '')

    def __unicode__(self):
        return "%s from %s @ (%s, %s)" % (self.full_name, self.loc, str(self.lat), str(self.lng))


class Commit(models.Model):
    repo = models.ForeignKey(Repo)
    actor = models.ForeignKey(Actor)
    hexsha = models.CharField(max_length=255, unique = True)



class Function(models.Model):
    name = models.CharField(max_length=255)
    commit = models.ForeignKey(Commit)