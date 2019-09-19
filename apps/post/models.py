from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import os
import random

# from django.utils.html import mark_safe
# from markdown import markdown
# from django.utils.text import Truncator


def get_filename_ext(filepath):
	base_name=os.path.basename(filepath)
	name,ext=os.path.splitext(base_name)
	return name,ext

def upload_image_path(instance, filename):
	new_filename=random.randint(1,3910209312)
	name,ext=get_filename_ext(filename)
	final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
	return "post-image/{final_filename}".format(
		new_filename=new_filename,
		final_filename=final_filename
		)


class Category(models.Model):
	name=models.CharField(max_length=20)
	slug=models.SlugField(max_length=100,unique=True,blank=True)

	def save(self, *args, **kwargs):
		self.slug=slugify(self.name)
		super(Category,self).save(*args,**kwargs)

	def __str__(self):
		return self.name


class Post(models.Model):
	STATUS_CHOICES=(
		('active','Active'),
		('in-active','In-active'),
		)
	title=models.CharField(max_length=30,unique=True)
	description=models.TextField(max_length=4000)
	categories=models.ManyToManyField(Category)
	image=models.ImageField(upload_to=upload_image_path,null=True,blank=False)
	created_at=models.DateTimeField(auto_now=False,auto_now_add=True)
	created_by=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
	slug=models.SlugField(max_length=100,unique=True,blank=True)
	status=models.CharField(max_length=50, choices=STATUS_CHOICES)
	views=models.PositiveIntegerField(default=0)
	featured=models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_comment_count(self):
		return Comment.objects.filter(post=self).count()

	# def get_page_count(self):
	# 	count=self.count()
	# 	pages= count/5
	# 	return math.ceil(pages)

	# def get_page_range(self):
	# 	count=self.get_page_count()
	# 	if self.has_many_pages(count):
	# 		return range(1,5)
	# 	return range(1, count+1)
	


	def save(self, *args, **kwargs):
		self.slug=slugify(self.title)
		super(Post,self).save(*args,**kwargs)

class Comment(models.Model):
	message=models.TextField(max_length=4000)
	post=models.ForeignKey(Post,related_name='posts',on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	created_by=models.ForeignKey(User, related_name='comments',on_delete=models.CASCADE)


    # def get_message_as_markdown(self):
    #     return mark_safe(markdown(self.message,safe_mode='escape'))