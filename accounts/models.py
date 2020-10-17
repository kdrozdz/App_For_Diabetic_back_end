from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class MyAccountManager(BaseUserManager):
	def create_user(self, email, last_name, first_name, age, profile, phone_number=None, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			last_name=last_name,
			first_name=first_name,
			age=age,
			profile=profile,
			phone_number=phone_number,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, last_name, first_name, age, profile,phone_number=None, password=None):
		user = self.create_user(
			email=self.normalize_email(email),
			last_name=last_name,
			first_name=first_name,
			age=age,
			profile=profile,
			phone_number=phone_number,
		)
		user.set_password(password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = None
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	last_name = models.CharField(max_length=32)
	first_name = models.CharField(max_length=32)
	age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
	profile = models.IntegerField(choices=((1, 'Doctor'), (2, 'Patient')))
	phone_number = models.IntegerField()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['last_name', 'first_name', 'profile', 'age', 'phone_number']

	objects = MyAccountManager()
	readonly_fields = ('id',)

	def __str__(self):
		return self.get_profile_display()

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
