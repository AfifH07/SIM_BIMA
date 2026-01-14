"""
Unit tests untuk Student views menggunakan pytest dan Django Test Client.
Testing GET dan POST requests pada endpoint siswa.
"""

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import date

from apps.users.models import User
from apps.students.models import Student


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def admin_user(db):
    """Create admin user untuk testing."""
    user = User.objects.create_user(
        email='admin@test.com',
        password='testpass123',
        full_name='Admin Test',
        role='ADMIN',
        is_staff=True
    )
    return user


@pytest.fixture
def teacher_user(db):
    """Create teacher user untuk testing."""
    user = User.objects.create_user(
        email='teacher@test.com',
        password='testpass123',
        full_name='Teacher Test',
        role='TEACHER'
    )
    return user


@pytest.fixture
def student_user(db):
    """Create student user untuk testing."""
    user = User.objects.create_user(
        email='student@test.com',
        password='testpass123',
        full_name='Student Test',
        role='STUDENT'
    )
    return user


@pytest.fixture
def admin_token(admin_user):
    """Create auth token untuk admin."""
    token, created = Token.objects.get_or_create(user=admin_user)
    return token.key


@pytest.fixture
def teacher_token(teacher_user):
    """Create auth token untuk teacher."""
    token, created = Token.objects.get_or_create(user=teacher_user)
    return token.key


@pytest.fixture
def sample_student(db):
    """Create sample student untuk testing."""
    student = Student.objects.create(
        nis='2023001',
        nisn='0012345678',
        full_name='Test Student',
        gender='M',
        date_of_birth=date(2005, 1, 1),
        place_of_birth='Jakarta',
        religion='Islam',
        address='Jl. Test No. 123',
        city='Jakarta',
        province='DKI Jakarta',
        parent_name='Parent Test',
        parent_phone='081234567890',
        admission_date=date(2023, 7, 1),
        status='ACTIVE'
    )
    return student


@pytest.mark.django_db
class TestStudentListView:
    """Test cases untuk GET /api/students/"""

    def test_list_students_without_auth(self, client):
        """Test list students tanpa autentikasi harus gagal."""
        url = '/api/students/'
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_students_with_auth(self, client, admin_token, sample_student):
        """Test list students dengan autentikasi harus berhasil."""
        url = '/api/students/'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0

    def test_list_students_empty(self, client, admin_token):
        """Test list students ketika tidak ada data."""
        url = '/api/students/'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_search_students(self, client, admin_token, sample_student):
        """Test search functionality."""
        url = '/api/students/?search=Test'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert 'Test' in data[0]['full_name']

    def test_filter_students_by_status(self, client, admin_token, sample_student):
        """Test filter students by status."""
        url = '/api/students/?status=ACTIVE'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(student['status'] == 'ACTIVE' for student in data)


@pytest.mark.django_db
class TestStudentDetailView:
    """Test cases untuk GET /api/students/{id}/"""

    def test_get_student_detail(self, client, admin_token, sample_student):
        """Test get detail student yang ada."""
        url = f'/api/students/{sample_student.id}/'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['nis'] == sample_student.nis
        assert data['full_name'] == sample_student.full_name

    def test_get_student_not_found(self, client, admin_token):
        """Test get detail student yang tidak ada."""
        url = '/api/students/99999/'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestStudentCreateView:
    """Test cases untuk POST /api/students/"""

    def test_create_student_success(self, client, admin_token):
        """Test create student dengan data valid."""
        url = '/api/students/'
        data = {
            'nis': '2024001',
            'nisn': '0012345679',
            'full_name': 'New Student',
            'gender': 'F',
            'date_of_birth': '2005-05-15',
            'place_of_birth': 'Bandung',
            'religion': 'Kristen',
            'address': 'Jl. New Test No. 456',
            'city': 'Bandung',
            'province': 'Jawa Barat',
            'parent_name': 'New Parent',
            'parent_phone': '081298765432',
            'admission_date': '2024-07-01',
        }

        response = client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data['nis'] == data['nis']
        assert response_data['full_name'] == data['full_name']

        # Verify student was created in database
        assert Student.objects.filter(nis='2024001').exists()

    def test_create_student_duplicate_nis(self, client, admin_token, sample_student):
        """Test create student dengan NIS yang sudah ada."""
        url = '/api/students/'
        data = {
            'nis': sample_student.nis,  # Duplicate NIS
            'nisn': '0012345680',
            'full_name': 'Another Student',
            'gender': 'M',
            'date_of_birth': '2005-03-20',
            'place_of_birth': 'Surabaya',
            'religion': 'Islam',
            'address': 'Jl. Test',
            'city': 'Surabaya',
            'province': 'Jawa Timur',
            'parent_name': 'Parent',
            'parent_phone': '081234567890',
            'admission_date': '2024-07-01',
        }

        response = client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'nis' in response.json()

    def test_create_student_missing_required_fields(self, client, admin_token):
        """Test create student dengan field yang kurang."""
        url = '/api/students/'
        data = {
            'nis': '2024002',
            'full_name': 'Incomplete Student',
            # Missing many required fields
        }

        response = client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_student_invalid_email(self, client, admin_token):
        """Test create student dengan email invalid."""
        url = '/api/students/'
        data = {
            'nis': '2024003',
            'nisn': '0012345681',
            'full_name': 'Test Invalid Email',
            'gender': 'M',
            'date_of_birth': '2005-01-01',
            'place_of_birth': 'Jakarta',
            'religion': 'Islam',
            'address': 'Jl. Test',
            'city': 'Jakarta',
            'province': 'DKI Jakarta',
            'parent_name': 'Parent',
            'parent_phone': '081234567890',
            'admission_date': '2024-07-01',
            'email': 'invalid-email',  # Invalid email
        }

        response = client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestStudentUpdateView:
    """Test cases untuk PUT/PATCH /api/students/{id}/"""

    def test_update_student_full(self, client, admin_token, sample_student):
        """Test full update student (PUT)."""
        url = f'/api/students/{sample_student.id}/'
        data = {
            'nis': sample_student.nis,
            'nisn': sample_student.nisn,
            'full_name': 'Updated Name',
            'gender': sample_student.gender,
            'date_of_birth': str(sample_student.date_of_birth),
            'place_of_birth': sample_student.place_of_birth,
            'religion': sample_student.religion,
            'address': 'Updated Address',
            'city': sample_student.city,
            'province': sample_student.province,
            'parent_name': sample_student.parent_name,
            'parent_phone': sample_student.parent_phone,
            'admission_date': str(sample_student.admission_date),
        }

        response = client.put(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data['full_name'] == 'Updated Name'
        assert response_data['address'] == 'Updated Address'

    def test_update_student_partial(self, client, admin_token, sample_student):
        """Test partial update student (PATCH)."""
        url = f'/api/students/{sample_student.id}/'
        data = {
            'phone_number': '081999999999'
        }

        response = client.patch(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data['phone_number'] == '081999999999'


@pytest.mark.django_db
class TestStudentDeleteView:
    """Test cases untuk DELETE /api/students/{id}/"""

    def test_delete_student(self, client, admin_token, sample_student):
        """Test delete student."""
        url = f'/api/students/{sample_student.id}/'
        response = client.delete(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK

        # Verify student was deleted
        assert not Student.objects.filter(id=sample_student.id).exists()


@pytest.mark.django_db
class TestStudentStatistics:
    """Test cases untuk endpoint statistik."""

    def test_get_statistics(self, client, admin_token, sample_student):
        """Test get student statistics."""
        url = '/api/students/statistics/'
        response = client.get(
            url,
            HTTP_AUTHORIZATION=f'Token {admin_token}'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'total' in data
        assert 'active' in data
        assert 'male' in data
        assert 'female' in data
