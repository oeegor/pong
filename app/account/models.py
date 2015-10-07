from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __unicode__(self):
        return u'{}'.format(self.email)

    def __repr__(self):
        return unicode(self)

    @property
    def short_email(self):
        return self.email.split('@')[0]
