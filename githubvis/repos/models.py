from django.db import models
from django.db.models.fields.related import ForeignKey

class BaseModel(models.Model):

	class Meta:
		abstract = True
	
	#i'm so sorry
	def to_dict(self, exclude_fields):
		these_fields = [f for f in exclude_fields if not '.' in f]
		next_fields = ['.'.join(f.split('.')[1:]) for f in exclude_fields]
		d = {field.name : getattr(self, field.name) for field in self._meta.fields if not getattr(getattr(self, field.name), 'to_dict', False) and not field.name in these_fields}
		d.update({field.name : getattr(self, field.name).to_dict(next_fields) for field in self._meta.fields if getattr(getattr(self, field.name), 'to_dict', False) and not field.name in these_fields})
		return d


# Create your models here.
class Repo(BaseModel):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    

class Actor(BaseModel):
    full_name = models.CharField(max_length=255)
    lat = models.FloatField(default = 0)   
    lng = models.FloatField(default = 0)
    loc = models.CharField(max_length = 255, default = '')

    def __unicode__(self):
        return "%s from %s @ (%s, %s)" % (self.full_name, self.loc, str(self.lat), str(self.lng))


class Commit(BaseModel):
    repo = models.ForeignKey(Repo)
    actor = models.ForeignKey(Actor)
    hexsha = models.CharField(max_length=255, unique = True)



class Function(BaseModel):
    name = models.CharField(max_length=512)
    commit = models.ForeignKey(Commit)
    path = models.CharField(max_length=512, default = '')


class FunctionCall(BaseModel):
    caller = models.ForeignKey(Function, related_name = 'function_call_caller')
    callee = models.ForeignKey(Function, related_name = 'function_call_callee')



class FileChange(BaseModel):
    commit = models.ForeignKey(Commit)
    path = models.CharField(max_length=512, default = '')
    actor = models.ForeignKey(Actor)

class CommonFileChange(BaseModel):
    change1 = models.ForeignKey(FileChange, related_name = 'file_changes1')
    change2 = models.ForeignKey(FileChange, related_name = 'file_change2')
