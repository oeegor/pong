from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __str__(self):
        return '{}'.format(self.email)

    def __repr__(self):
        return str(self)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def short_email(self):
        return self.email.split('@')[0]
