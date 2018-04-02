from __future__ import unicode_literals

import hashlib
import os.path
import urllib

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from socialmedia.activities.models import Notification


@python_2_unicode_compatible
class Profile(models.Model):

    PROFILE_TYPE = (
        ('P', _('Person')),
        ('B', _('Business')),
    )
    GENDER_OPTION =(
        ('M',_('Male')),
        ('F',_('Female'))
    )
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50, null=True, blank=True,verbose_name=_('Location'))
    url = models.CharField(max_length=50, null=True, blank=True,verbose_name=_('URL'))
    job_title = models.CharField(max_length=50, null=True, blank=True,verbose_name=_('Title'))
    birthday = models.DateField(null=True, blank=True,verbose_name=_('Birthday'))
    profile_type = models.CharField(max_length=2, null=True, blank=True,choices=PROFILE_TYPE,default='P',verbose_name=_('Type'))
    budge = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True,verbose_name=_('Budge'))
    about_text = models.TextField(verbose_name=_('About'))
    gender = models.CharField(max_length=2, null=True, blank=True,choices=GENDER_OPTION,verbose_name=_('Gender'))

    class Meta:
        db_table = 'auth_profile'

    def age(self):
        try:
            import datetime
            return int((datetime.date.today() - self.birthday).days / 365.25)
        except:
            return 0

    def __str__(self):
        return self.user.username

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:  # noqa: E501
            url = "http://" + str(self.url)

        return url

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '.jpg'
            if os.path.isfile(filename):  # pragma: no cover
                return picture_url
            else:  # pragma: no cover
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_picture


    def get_bg_picture(self):
        no_bg_picture = 'http://placehold.it/1030x360'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '_bg_tmp.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '_bg_tmp.jpg'

            if os.path.isfile(filename):  # pragma: no cover
                im = Image.open(filename)
                im2 = im.crop((0, 0, 1030, 360))
                crop_filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '_bg_1030_tmp.jpg'
                crop_picture_url = settings.MEDIA_URL + 'profile_pictures/' + \
                              self.user.username + '_bg_1030_tmp.jpg'
                if not os.path.isfile(crop_filename):
                    im2.save(crop_filename)
                #return picture_url
                return crop_picture_url
            else:  # pragma: no cover
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_bg_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_bg_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:  # pragma: no cover
            return self.user.username

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user, to_user=feed.user,
                                        feed=feed).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)

        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user), feed=feed).save()

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                         from_user=self.user, to_user=question.user,
                         question=question).save()

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(
                notification_type=Notification.FAVORITED,
                from_user=self.user,
                to_user=question.user,
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(
                notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user,
                to_user=answer.user,
                answer=answer).delete()

    def get_messages_amount(self):

        from socialmedia.messenger.models import Message
        from django.db.models import Q

        return Message.objects.filter(
        Q(from_user=self.user) | Q(user=self.user)).count()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
