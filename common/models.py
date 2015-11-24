from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class BaseModel(models.Model):
	creator = models.ForeignKey(User,related_name = '%(app_label)s_%(class)s_created_by')
	#created_date = models.DateTimeField(auto_now_add=True,auto_now=False, default=timezone.now)
	#modified_date = models.DateTimeField(auto_now=True,auto_now_add=False, default=timezone.now)
	editor = models.ForeignKey(User, null=True, blank=True, related_name='%(app_label)s_%(class)s_last_modified')

	def __str__(self):
		return self.creator.get_full_name()

	class Meta:
		abstract = True

#tagged item consists like as well as review features
class Item(models.Model):
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		abstract = True
		unique_together = ("content_type", 'object_id')

	def __unicode__(self):
		return '%s' % (self.content_object)

class RangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
    	self.min_value, self.max_value = min_value, max_value
    	models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
    	defaults = {'min_value': self.min_value, 'max_value':self.max_value}
    	defaults.update(kwargs)
    	return super(RangeField, self).formfield(**defaults)