"""
User model untuk SIM SMA BIMA.
Mendukung berbagai role: Admin, Guru, Siswa, dan Orang Tua.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager untuk model User."""

    def create_user(self, email, password=None, **extra_fields):
        """Membuat dan menyimpan user biasa."""
        if not email:
            raise ValueError('Email harus diisi')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Membuat dan menyimpan superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model dengan email sebagai username.
    Mendukung role-based access control.
    """

    ROLE_CHOICES = [
        ('ADMIN', 'Admin Sekolah'),
        ('TEACHER', 'Guru'),
        ('STUDENT', 'Siswa'),
        ('PARENT', 'Orang Tua'),
    ]

    # Fields utama
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        db_index=True
    )
    full_name = models.CharField(
        verbose_name='Nama Lengkap',
        max_length=255
    )
    role = models.CharField(
        verbose_name='Role',
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )

    # Fields tambahan
    phone_number = models.CharField(
        verbose_name='Nomor Telepon',
        max_length=20,
        blank=True,
        null=True
    )
    address = models.TextField(
        verbose_name='Alamat',
        blank=True,
        null=True
    )
    photo = models.ImageField(
        verbose_name='Foto Profil',
        upload_to='users/photos/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        verbose_name='Tanggal Lahir',
        blank=True,
        null=True
    )

    # Status fields
    is_active = models.BooleanField(
        verbose_name='Aktif',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Staff',
        default=False
    )
    is_verified = models.BooleanField(
        verbose_name='Terverifikasi',
        default=False
    )

    # Timestamp fields
    date_joined = models.DateTimeField(
        verbose_name='Tanggal Bergabung',
        default=timezone.now
    )
    last_login = models.DateTimeField(
        verbose_name='Login Terakhir',
        blank=True,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    def get_short_name(self):
        """Return nama pendek user."""
        return self.full_name.split()[0] if self.full_name else self.email

    @property
    def is_admin(self):
        """Check apakah user adalah admin."""
        return self.role == 'ADMIN'

    @property
    def is_teacher(self):
        """Check apakah user adalah guru."""
        return self.role == 'TEACHER'

    @property
    def is_student(self):
        """Check apakah user adalah siswa."""
        return self.role == 'STUDENT'

    @property
    def is_parent(self):
        """Check apakah user adalah orang tua."""
        return self.role == 'PARENT'
