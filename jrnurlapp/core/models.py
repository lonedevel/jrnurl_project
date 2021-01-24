from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
import uuid


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if email is None:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class URLCollection(models.Model):
    CAPTURED = 100
    TECHNICAL = 200
    NEWS = 300
    RESEARCH = 400
    GAMES = 500
    HUMOR = 600
    OTHER = 900
    COLLECTION_TYPE_CHOICES = [
        (CAPTURED, 'Captured'),
        (TECHNICAL, 'Technical'),
        (NEWS, 'News'),
        (RESEARCH, 'Research'),
        (GAMES, 'Games'),
        (HUMOR, 'Humor'),
        (OTHER, 'Other')
    ]
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=now, blank=True)
    modified = models.DateTimeField(default=now, blank=True)
    collection_type = models.IntegerField(choices=COLLECTION_TYPE_CHOICES,
                                          default=CAPTURED)
    favorite = models.BooleanField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=45),
                      null=True,
                      blank=True, size=25)
    items = models.ManyToManyField('URLItem', through='URLCollectionItems')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_collection_type_display()} - {self.name}'

    class Meta:
        ordering = ['name']
        verbose_name_plural = "URL Collections"


class URLItem(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=2048)
    visits = models.IntegerField()
    created = models.DateTimeField(blank=True,
                                   null=True,
                                   default=now)
    modified = models.DateTimeField(blank=True,
                                    null=True,
                                    default=now)
    tags = ArrayField(models.CharField(max_length=45),
                      null=True,
                      blank=True)
    collection = models.ManyToManyField('URLCollection',
                                        through='URLCollectionItems')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "URL Items"


class URLCollectionItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey(URLCollection,
                                   on_delete=models.CASCADE)
    item = models.ForeignKey(URLItem,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.collection.name + ': ' + self.item.title

    class Meta:
        verbose_name_plural = "URL Collection Items"
