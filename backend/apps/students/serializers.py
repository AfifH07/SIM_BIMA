"""
Serializers untuk Student app.
Mengonversi data model ke JSON dan validasi input.
"""

from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer untuk model Student."""

    # Read-only computed fields
    age = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    full_address = serializers.SerializerMethodField()

    # Display fields
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'nis',
            'nisn',
            'full_name',
            'nickname',
            'gender',
            'gender_display',
            'date_of_birth',
            'place_of_birth',
            'religion',
            'blood_type',
            'address',
            'city',
            'province',
            'postal_code',
            'phone_number',
            'email',
            'parent_name',
            'parent_phone',
            'parent_email',
            'parent_occupation',
            'parent_address',
            'admission_date',
            'graduation_date',
            'status',
            'status_display',
            'class_room',
            'photo',
            'age',
            'is_active',
            'full_address',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_address(self, obj):
        """Return full address with city and province."""
        return obj.get_full_address()

    def validate_nis(self, value):
        """Validasi NIS unik."""
        if self.instance and self.instance.nis == value:
            return value

        if Student.objects.filter(nis=value).exists():
            raise serializers.ValidationError("NIS sudah digunakan.")
        return value

    def validate_nisn(self, value):
        """Validasi NISN unik."""
        if not value:
            return value

        if self.instance and self.instance.nisn == value:
            return value

        if Student.objects.filter(nisn=value).exists():
            raise serializers.ValidationError("NISN sudah digunakan.")
        return value

    def validate_email(self, value):
        """Validasi email format."""
        if value and '@' not in value:
            raise serializers.ValidationError("Format email tidak valid.")
        return value

    def validate_phone_number(self, value):
        """Validasi nomor telepon."""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Nomor telepon hanya boleh berisi angka, +, -, dan spasi.")
        return value

    def validate(self, data):
        """Validasi cross-field."""
        # Validasi tanggal lahir tidak boleh di masa depan
        if 'date_of_birth' in data:
            from datetime import date
            if data['date_of_birth'] > date.today():
                raise serializers.ValidationError({
                    'date_of_birth': 'Tanggal lahir tidak boleh di masa depan.'
                })

        # Validasi tanggal lulus harus setelah tanggal masuk
        if 'graduation_date' in data and data.get('graduation_date'):
            admission_date = data.get('admission_date', getattr(self.instance, 'admission_date', None))
            if admission_date and data['graduation_date'] < admission_date:
                raise serializers.ValidationError({
                    'graduation_date': 'Tanggal lulus harus setelah tanggal masuk.'
                })

        return data


class StudentListSerializer(serializers.ModelSerializer):
    """Serializer ringkas untuk list view."""

    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = [
            'id',
            'nis',
            'full_name',
            'gender',
            'gender_display',
            'age',
            'status',
            'status_display',
            'class_room',
            'phone_number',
            'email',
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer untuk create student."""

    class Meta:
        model = Student
        fields = [
            'nis',
            'nisn',
            'full_name',
            'nickname',
            'gender',
            'date_of_birth',
            'place_of_birth',
            'religion',
            'blood_type',
            'address',
            'city',
            'province',
            'postal_code',
            'phone_number',
            'email',
            'parent_name',
            'parent_phone',
            'parent_email',
            'parent_occupation',
            'parent_address',
            'admission_date',
            'photo',
        ]

    def validate_nis(self, value):
        """Validasi NIS unik."""
        if Student.objects.filter(nis=value).exists():
            raise serializers.ValidationError("NIS sudah digunakan.")
        return value

    def validate_nisn(self, value):
        """Validasi NISN unik."""
        if value and Student.objects.filter(nisn=value).exists():
            raise serializers.ValidationError("NISN sudah digunakan.")
        return value
