"""
Student model untuk SIM SMA BIMA.
Mengelola data siswa dan informasi akademik.
"""

from django.db import models
from django.conf import settings


class Student(models.Model):
    """Model untuk data siswa."""

    GENDER_CHOICES = [
        ('M', 'Laki-laki'),
        ('F', 'Perempuan'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('GRADUATED', 'Lulus'),
        ('DROPPED', 'Keluar'),
        ('SUSPENDED', 'Diskors'),
    ]

    # Relasi dengan User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='User',
        null=True,
        blank=True
    )

    # Data Pribadi
    nis = models.CharField(
        verbose_name='NIS',
        max_length=20,
        unique=True,
        db_index=True
    )
    nisn = models.CharField(
        verbose_name='NISN',
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    full_name = models.CharField(
        verbose_name='Nama Lengkap',
        max_length=255
    )
    nickname = models.CharField(
        verbose_name='Nama Panggilan',
        max_length=100,
        blank=True,
        null=True
    )
    gender = models.CharField(
        verbose_name='Jenis Kelamin',
        max_length=1,
        choices=GENDER_CHOICES
    )
    date_of_birth = models.DateField(
        verbose_name='Tanggal Lahir'
    )
    place_of_birth = models.CharField(
        verbose_name='Tempat Lahir',
        max_length=100
    )
    religion = models.CharField(
        verbose_name='Agama',
        max_length=50
    )
    blood_type = models.CharField(
        verbose_name='Golongan Darah',
        max_length=3,
        blank=True,
        null=True
    )

    # Alamat & Kontak
    address = models.TextField(
        verbose_name='Alamat Lengkap'
    )
    city = models.CharField(
        verbose_name='Kota/Kabupaten',
        max_length=100
    )
    province = models.CharField(
        verbose_name='Provinsi',
        max_length=100
    )
    postal_code = models.CharField(
        verbose_name='Kode Pos',
        max_length=10,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        verbose_name='Nomor Telepon',
        max_length=20,
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=True,
        null=True
    )

    # Data Orang Tua/Wali
    parent_name = models.CharField(
        verbose_name='Nama Orang Tua/Wali',
        max_length=255
    )
    parent_phone = models.CharField(
        verbose_name='Nomor Telepon Orang Tua',
        max_length=20
    )
    parent_email = models.EmailField(
        verbose_name='Email Orang Tua',
        blank=True,
        null=True
    )
    parent_occupation = models.CharField(
        verbose_name='Pekerjaan Orang Tua',
        max_length=100,
        blank=True,
        null=True
    )
    parent_address = models.TextField(
        verbose_name='Alamat Orang Tua',
        blank=True,
        null=True
    )

    # Data Akademik
    admission_date = models.DateField(
        verbose_name='Tanggal Masuk'
    )
    graduation_date = models.DateField(
        verbose_name='Tanggal Lulus',
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    class_room = models.ForeignKey(
        'classes.ClassRoom',
        on_delete=models.SET_NULL,
        related_name='students',
        verbose_name='Kelas',
        null=True,
        blank=True
    )

    # Foto
    photo = models.ImageField(
        verbose_name='Foto',
        upload_to='students/photos/',
        blank=True,
        null=True
    )

    # Metadata
    created_at = models.DateTimeField(
        verbose_name='Dibuat Pada',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Diperbarui Pada',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Siswa'
        verbose_name_plural = 'Siswa'
        ordering = ['full_name']
        indexes = [
            models.Index(fields=['nis']),
            models.Index(fields=['nisn']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.nis} - {self.full_name}"

    @property
    def age(self):
        """Menghitung umur siswa."""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def is_active(self):
        """Check apakah siswa aktif."""
        return self.status == 'ACTIVE'

    def get_full_address(self):
        """Return alamat lengkap dengan kota dan provinsi."""
        return f"{self.address}, {self.city}, {self.province}"
