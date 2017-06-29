from django.db import models
from django.contrib.auth.models import User

#---------------------------------作业代码（开始）-------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

#---------------------------------作业代码（结束）-------------------------------

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image', null=True)

#---------------------------------作业代码（开始）-------------------------------
    is_InvitedAuthor = models.BooleanField(default=False)
    is_Banned = models.BooleanField(default=False)

#---------------------------------作业代码（结束）-------------------------------

    def __str__(self):
        return self.belong_to.username

#---------------------------------作业代码（开始）-------------------------------
#注：这种方法结合view来创建
#详见：https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
#及见：https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(belong_to=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#注：这种方法注册不会创建，只有登录了才会创建
# User.profile = property(lambda u: UserProfile.objects.get_or_create(belong_to=u)[0])

#---------------------------------作业代码（结束）-------------------------------

class Video(models.Model):
    title = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    cover = models.FileField(upload_to='cover_image', null=True)
    editors_choice = models.BooleanField(default=False)
    owner = models.ForeignKey(to=UserProfile, related_name='videos', default=1)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    video = models.ForeignKey(to=Video, related_name='tickets')
    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal'),
        )
    choice = models.CharField(choices=VOTE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)
