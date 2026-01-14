"""
Custom middleware untuk SIM SMA BIMA.
Menangani autentikasi token dan security checks.
"""

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware untuk validasi token autentikasi.
    Memeriksa Authorization header pada setiap request API.
    """

    def process_request(self, request):
        """
        Process request untuk validasi token.
        """
        # Skip authentication untuk endpoints publik
        public_paths = [
            '/admin/',
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/docs/',
            '/api/schema/',
        ]

        # Check jika path adalah public
        if any(request.path.startswith(path) for path in public_paths):
            return None

        # Skip untuk non-API requests
        if not request.path.startswith('/api/'):
            return None

        # Get token dari header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            # Jika tidak ada token, Django REST Framework akan handle
            return None

        # Parse token
        try:
            # Format: "Token <token_value>" atau "Bearer <token_value>"
            parts = auth_header.split()

            if len(parts) != 2:
                return JsonResponse(
                    {'error': 'Format Authorization header tidak valid. Gunakan: Token <token>'},
                    status=401
                )

            token_type = parts[0]
            token_value = parts[1]

            # Support both "Token" and "Bearer" prefix
            if token_type.lower() not in ['token', 'bearer']:
                return JsonResponse(
                    {'error': 'Tipe token tidak valid. Gunakan: Token atau Bearer'},
                    status=401
                )

            # Validasi token
            try:
                token = Token.objects.select_related('user').get(key=token_value)

                # Check apakah user masih aktif
                if not token.user.is_active:
                    return JsonResponse(
                        {'error': 'User tidak aktif.'},
                        status=403
                    )

                # Attach user ke request
                request.user = token.user

            except Token.DoesNotExist:
                return JsonResponse(
                    {'error': 'Token tidak valid atau sudah expired.'},
                    status=401
                )

        except Exception as e:
            return JsonResponse(
                {'error': f'Error validasi token: {str(e)}'},
                status=401
            )

        return None


class RoleBasedAccessMiddleware(MiddlewareMixin):
    """
    Middleware untuk role-based access control.
    Membatasi akses berdasarkan role user.
    """

    def process_request(self, request):
        """
        Check role-based permissions.
        """
        # Skip untuk non-authenticated users (akan di-handle oleh Django)
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return None

        # Admin bypass semua restrictions
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return None

        # Define role-based access rules
        role_restrictions = {
            'STUDENT': {
                'forbidden_paths': [
                    '/api/users/',
                    '/api/teachers/',
                    '/api/finance/payments/',  # Siswa hanya bisa lihat payment mereka sendiri
                ],
            },
            'TEACHER': {
                'forbidden_paths': [
                    '/api/users/',
                    '/api/finance/reports/',  # Guru tidak bisa akses laporan keuangan
                ],
            },
            'PARENT': {
                'forbidden_paths': [
                    '/api/users/',
                    '/api/teachers/',
                    '/api/classes/',
                    '/api/grades/input/',  # Parent hanya bisa view, tidak bisa input
                ],
            },
        }

        user_role = request.user.role
        if user_role in role_restrictions:
            restrictions = role_restrictions[user_role]
            forbidden_paths = restrictions.get('forbidden_paths', [])

            for forbidden_path in forbidden_paths:
                if request.path.startswith(forbidden_path):
                    # Allow GET for some paths
                    if request.method in ['GET', 'HEAD', 'OPTIONS']:
                        continue

                    return JsonResponse(
                        {
                            'error': 'Anda tidak memiliki akses ke resource ini.',
                            'detail': f'Role {user_role} tidak diizinkan mengakses {forbidden_path}'
                        },
                        status=403
                    )

        return None


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware untuk logging request API.
    Berguna untuk audit trail dan debugging.
    """

    def process_request(self, request):
        """Log incoming requests."""
        # Skip logging untuk static files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None

        # Log hanya untuk API requests
        if request.path.startswith('/api/'):
            import logging
            logger = logging.getLogger('django')

            user = 'Anonymous'
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user.email

            logger.info(
                f"API Request: {request.method} {request.path} | User: {user} | IP: {self.get_client_ip(request)}"
            )

        return None

    def process_response(self, request, response):
        """Log responses with status codes."""
        if request.path.startswith('/api/'):
            import logging
            logger = logging.getLogger('django')

            # Log errors
            if response.status_code >= 400:
                logger.warning(
                    f"API Response: {request.method} {request.path} | Status: {response.status_code}"
                )

        return response

    @staticmethod
    def get_client_ip(request):
        """Get client IP address dari request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
