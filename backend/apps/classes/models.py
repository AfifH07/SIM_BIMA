"""
ClassRoom model untuk SIM SMA BIMA.
Mengelola data kelas dan jadwal.
"""

from django.db import models


class ClassRoom(models.Model):
    """Model untuk data kelas/ruang kelas."""

    GRADE_LEVEL_CHOICES = [
        (10, 'Kelas X'),
        (11, 'Kelas XI'),
        (12, 'Kelas XII'),
    ]

    # Basic Information
    name = models.CharField(
        verbose_name='Nama Kelas',
        max_length=50,
        unique=True,
        help_text='Contoh: XII IPA 1'
    )
    grade_level = models.IntegerField(
        verbose_name='Tingkat Kelas',
        choices=GRADE_LEVEL_CHOICES
    )
    academic_year = models.CharField(
        verbose_name='Tahun Ajaran',
        max_length=10,
        help_text='Contoh: 2023/2024'
    )

    # Teacher Assignment
    homeroom_teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        related_name='homeroom_classes',
        verbose_name='Wali Kelas',
        null=True,
        blank=True
    )

    # Class Details
    capacity = models.IntegerField(
        verbose_name='Kapasitas',
        default=36,
        help_text='Jumlah maksimal siswa'
    )
    room_number = models.CharField(
        verbose_name='Nomor Ruangan',
        max_length=20,
        null=True,
        blank=True
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
        verbose_name = 'Kelas'
        verbose_name_plural = 'Kelas'
        ordering = ['grade_level', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['grade_level']),
        ]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

    @property
    def student_count(self):
        """Return jumlah siswa dalam kelas."""
        return self.students.filter(status='ACTIVE').count()

    @property
    def is_full(self):
        """Check apakah kelas sudah penuh."""
        return self.student_count >= self.capacity

    @property
    def available_seats(self):
        """Return jumlah kursi yang tersedia."""
        return max(0, self.capacity - self.student_count)


class Subject(models.Model):
    """Model untuk mata pelajaran."""

    CATEGORY_CHOICES = [
        ('UMUM', 'Mata Pelajaran Umum'),
        ('PEMINATAN', 'Mata Pelajaran Peminatan'),
        ('LINTAS_MINAT', 'Mata Pelajaran Lintas Minat'),
    ]

    code = models.CharField(
        verbose_name='Kode',
        max_length=20,
        unique=True
    )
    name = models.CharField(
        verbose_name='Nama Mata Pelajaran',
        max_length=100
    )
    category = models.CharField(
        verbose_name='Kategori',
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    description = models.TextField(
        verbose_name='Deskripsi',
        blank=True,
        null=True
    )
    credits = models.IntegerField(
        verbose_name='SKS',
        default=2
    )

    created_at = models.DateTimeField(
        verbose_name='Dibuat Pada',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Mata Pelajaran'
        verbose_name_plural = 'Mata Pelajaran'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class ClassSubject(models.Model):
    """Model untuk relasi kelas dengan mata pelajaran dan jadwal."""

    DAY_CHOICES = [
        ('SENIN', 'Senin'),
        ('SELASA', 'Selasa'),
        ('RABU', 'Rabu'),
        ('KAMIS', 'Kamis'),
        ('JUMAT', 'Jumat'),
        ('SABTU', 'Sabtu'),
    ]

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='class_subjects',
        verbose_name='Kelas'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_subjects',
        verbose_name='Mata Pelajaran'
    )
    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        related_name='teaching_subjects',
        verbose_name='Guru Pengajar',
        null=True,
        blank=True
    )

    # Schedule
    schedule_day = models.CharField(
        verbose_name='Hari',
        max_length=10,
        choices=DAY_CHOICES,
        null=True,
        blank=True
    )
    schedule_time = models.TimeField(
        verbose_name='Waktu',
        null=True,
        blank=True,
        help_text='Waktu mulai pelajaran'
    )
    duration = models.IntegerField(
        verbose_name='Durasi (menit)',
        default=90,
        help_text='Durasi pelajaran dalam menit'
    )

    created_at = models.DateTimeField(
        verbose_name='Dibuat Pada',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Jadwal Mata Pelajaran'
        verbose_name_plural = 'Jadwal Mata Pelajaran'
        ordering = ['schedule_day', 'schedule_time']
        unique_together = [['classroom', 'subject']]

    def __str__(self):
        return f"{self.classroom.name} - {self.subject.name}"
