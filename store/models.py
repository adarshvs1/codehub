from django.db import models

from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

from django.db.models.signals import post_save  #used to create profile automatically

from django.db.models import Avg  #used to average


#Create your models here

#User Profile

class UserProfile(models.Model):

    bio=models.CharField(max_length=260,null=True)

    profile_pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.user_object.username
    

#Tag

class Tag(models.Model):

    title=models.CharField(max_length=200,unique=True) #unique used to avoid duplication

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
     
    def __str__(self):

        return self.title
    

#project

class Project(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField()

    tag_objects=models.ManyToManyField(Tag)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="projects")

    thumbnail=EmbedVideoField()

    price=models.PositiveIntegerField()

    files=models.FileField(upload_to="projects",null=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def downloads(self):  #is used to see the dowloads count of the project
        
        return OrderSummary.objects.filter(is_paid=True,project_objects=self).count()
    
    @property
    def review_count(self):  #is used to see the review of the project

        return self.project_reviews.all().count()
    
    @property
    def average_rating(self):   #used to see the avg rating

        return self.project_reviews.all().values('rating').aggregate(avg=Avg('rating')).get('avg',0)

    def __str__(self):

        return self.title
    
   
    
#WishList    

from django.db.models import Sum    #is used to see tha total amount of your cart items

class WishList(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def wishlist_total(self):   #is used to get logged user wishlist(cart) total amount

        return self.basket_items.filter(is_order_placed=False).values('project_object__price').aggregate(total=Sum('project_object__price')).get('total')

#Wishlist Items

class WishListItems(models.Model):

    wishlist_object=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="basket_items")

    project_object=models.ForeignKey(Project,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

#Order Summary

class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')

    project_objects=models.ManyToManyField(Project)

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total=models.FloatField(null=True)   #total amount


#profile creating

def create_profile(sender,instance,created,*args,**kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)  

post_save.connect(sender=User,receiver=create_profile)  #after registration automatically create profile

#python manage.py create superuser   

#basket create

def create_basket(sender,instance,created,*args,**kwargs):

    if created:

        WishList.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)



#reviews model

from django.core.validators import MaxValueValidator,MinValueValidator #is used to maximum number and minimum number

class Reviews(models.Model):

    project_object= models.ForeignKey(Project,on_delete=models.CASCADE,related_name='project_reviews')

    user_object= models.ForeignKey(User,on_delete=models.CASCADE)

    comment= models.TextField()

    rating = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)]) #star rating 1 to 5

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
