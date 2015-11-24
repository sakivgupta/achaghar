# Create your models here
from django.db import models
from django.contrib.auth.models import User,Group
from common.models import BaseModel,Item,RangeField
from django.utils import timezone
import os
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from autoslug import AutoSlugField


class Image(Item):
    image = models.ImageField(upload_to='images/')
    
    def __unicode__(self):
        return '%s' % (self.image.name)

class ImageAltHref(Image):
    alt = models.CharField(max_length=50, null=True, blank=True, default='',verbose_name='Alt text',help_text='Text to display in case image does not load')
    href = models.CharField(max_length=200, null=True, blank=True, default='',verbose_name='URL', help_text='Enter full URL to link to, with trailing slash (e.g. http://www.achaghar.com/xyz/)')

    class Meta:
        verbose_name = 'Image Link'
        ordering = ('id', )

class Country(models.Model):
	country = models.CharField(max_length=30,default='India',verbose_name="Country")
	flag = models.CharField(max_length=10, verbose_name="Flag Icons",blank=True,null=True)
	tel_code = models.CharField(max_length=10, verbose_name="Telephone Codes",blank=True,null=True)
	currency = models.CharField(max_length=20, verbose_name="Default Currency",blank=True,null=True,default="INR")

	def __str__(self):
		return self.country	

class Address(models.Model):
	add1 = models.CharField(max_length = 50)
	add2 = models.CharField(max_length = 50, null = True, blank = True)
	pincode = models.CharField(max_length=6, help_text="Pincode must be Six digits only",verbose_name="Pincode")
	city = models.CharField(max_length=50, verbose_name="City",blank=True)
	locality = models.CharField(max_length=50, verbose_name="Locality",blank=True)
	state = models.CharField(max_length=50, verbose_name="State",blank=True)
	country=models.ForeignKey(Country)
	
	def __str__(self):
		return "address1 = %s , city = %s , state = %s , pincode = %s, country = %s"%(self.add1,self.city,self.state,self.pincode,self.country)

class Type(models.Model):
	user_type = models.CharField(max_length=1,choices=(('B', 'Broker'), ('O', 'Owner'), ('FR', 'Flatmate Required'),),default='O')

	def __str__(self):
		return user_type

class UserProfile(BaseModel):
	user = models.ForeignKey(User)
	address = models.ForeignKey(Address,null=True,blank=True)
	mobile = models.IntegerField(help_text="Phone number must be 10 digits entered without +91",verbose_name="Mobile Number")
	phone = models.CharField(blank=True, null=True, max_length=15)
	ip = models.CharField(blank=True, null=True, max_length=50, default="") #store real ip from  requests meta field
	country = models.ForeignKey(Country,default="India")
	subscribed = models.BooleanField(default=True)
	info = models.CharField(max_length=100,blank=True,null=True)

	def unsubscribe_link(self):
		'''create a hashed unsubscribed link for the newsletter and use url to join with it and pass it to users'''

		link = str(self.user.email)+str(self.user.id)
		return urlsafe_base64_encode(link)
	
	def _get_username_profile(self):
		return "Username - %s , Profile - %s"%(self.user.username,self.user.get_full_name())

	full_name = property(_get_username_profile)
	link = property(unsubscribe_link)

	def __str__(self):
		return self.full_name

	class Meta:
		ordering = ['user']

class General(models.Model):
	features = models.CharField(max_length=200,verbose_name="Add Features")
	current_residents = models.IntegerField(blank=True,default=0,null=False,verbose_name="Current Residents")
	residents_info = models.CharField(max_length=100,blank=False,null=False,verbose_name="Residents Information")
	looking_for_info = models.CharField(max_length=200,blank=False,null=False,verbose_name="Looking For")
	rent = models.IntegerField()
	flat_type = models.CharField(blank=True,null=True,max_length=10,default='1 BHK')
	add_payment = models.CharField(max_length=100,blank=True,null=True,verbose_name="Additional Payment")
	services = models.CharField(max_length=200,blank=True,null=True)
	images = models.ManyToManyField(Image, default=None, related_name="room_images" ,blank=True, help_text="")

	class Meta:
		abstract = True

class Category(models.Model):
	choices = (('F','Flat'),('PG-G','PG Girls'),('PG-B','PG Boys'),('R','Rooms'),)
	post_type = models.CharField(max_length=1,choices=choices,default='F',verbose_name="Post Type")

	def __str__(self):
		return post_type

class Post(BaseModel,General):
	user = models.ForeignKey(UserProfile,verbose_name='Add Posted By')
	user_type = models.ForeignKey(Type)
	category = models.ForeignKey(Category)
	location = models.ForeignKey(Address)
	alternate_mobile = models.IntegerField(help_text="Phone number must be 10 digits entered without +91", verbose_name="Alternate Mobile",blank=True,null=True)
	
class Reviews(Item):
	user = models.ForeignKey(User)
	room = models.ForeignKey(Post)
	review = models.CharField(max_length=100)	

	def __str__(self):
		return '%s - %s - %s - %s' % (self.user, self.room, self.review, self.content_object, )

	class Meta:
		unique_together = ('user','room')