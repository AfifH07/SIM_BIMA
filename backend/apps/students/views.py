"""
Views untuk Student app.
REST API untuk CRUD operations siswa.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Student
from .serializers import (
    StudentSerializer,
    StudentListSerializer,
    StudentCreateSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk CRUD operations Student.

    Endpoints:
    - GET /api/students/ - List semua siswa
    - POST /api/students/ - Tambah siswa baru
    - GET /api/students/{id}/ - Detail siswa
    - PUT /api/students/{id}/ - Update siswa
    - PATCH /api/students/{id}/ - Partial update siswa
    - DELETE /api/students/{id}/ - Hapus siswa
    - GET /api/students/active/ - List siswa aktif
    - GET /api/students/search/?q=keyword - Search siswa
    """

    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nis', 'nisn', 'full_name', 'email', 'parent_name']
    ordering_fields = ['full_name', 'nis', 'admission_date', 'created_at']
    ordering = ['full_name']

    def get_serializer_class(self):
        """Return serializer class berdasarkan action."""
        if self.action == 'list':
            return StudentListSerializer
        elif self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer

    def get_queryset(self):
        """Filter queryset berdasarkan query parameters."""
        queryset = super().get_queryset()

        # Filter by status
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param.upper())

        # Filter by class
        class_id = self.request.query_params.get('class_id', None)
        if class_id:
            queryset = queryset.filter(class_room_id=class_id)

        # Filter by gender
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender.upper())

        # Search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(nis__icontains=search) |
                Q(nisn__icontains=search) |
                Q(email__icontains=search) |
                Q(parent_name__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        """Create student baru."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Return dengan serializer lengkap
        student = Student.objects.get(pk=serializer.instance.pk)
        output_serializer = StudentSerializer(student)

        headers = self.get_success_headers(serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Update student."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # Return dengan serializer lengkap
        output_serializer = StudentSerializer(instance)
        return Response(output_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete student."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Siswa berhasil dihapus.'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get list siswa aktif saja."""
        queryset = self.get_queryset().filter(status='ACTIVE')
        serializer = StudentListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get statistik siswa."""
        queryset = self.get_queryset()

        stats = {
            'total': queryset.count(),
            'active': queryset.filter(status='ACTIVE').count(),
            'graduated': queryset.filter(status='GRADUATED').count(),
            'dropped': queryset.filter(status='DROPPED').count(),
            'suspended': queryset.filter(status='SUSPENDED').count(),
            'male': queryset.filter(gender='M').count(),
            'female': queryset.filter(gender='F').count(),
        }

        return Response(stats)

    @action(detail=True, methods=['post'])
    def graduate(self, request, pk=None):
        """Tandai siswa sebagai lulus."""
        student = self.get_object()

        from datetime import date
        student.status = 'GRADUATED'
        student.graduation_date = date.today()
        student.save()

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Aktifkan siswa."""
        student = self.get_object()
        student.status = 'ACTIVE'
        student.save()

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export data siswa ke CSV (simplified)."""
        queryset = self.get_queryset()

        # Untuk implementasi lengkap, gunakan library seperti django-import-export
        # Ini hanya contoh response
        data = []
        for student in queryset:
            data.append({
                'nis': student.nis,
                'nama': student.full_name,
                'jenis_kelamin': student.get_gender_display(),
                'tanggal_lahir': student.date_of_birth,
                'status': student.get_status_display(),
                'email': student.email or '',
                'telepon': student.phone_number or '',
            })

        return Response(data)
