"""
User management utilities untuk SIM SMA BIMA.
Fungsi-fungsi untuk membuat, mengedit, menghapus, login, dan logout user.
"""

from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework.authtoken.models import Token
from typing import Dict, Optional, Tuple

User = get_user_model()


class UserManagement:
    """Class untuk mengelola operasi user."""

    @staticmethod
    def create_user(
        email: str,
        password: str,
        full_name: str,
        role: str,
        **extra_fields
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Membuat user baru.

        Args:
            email: Email user
            password: Password user
            full_name: Nama lengkap user
            role: Role user (ADMIN, TEACHER, STUDENT, PARENT)
            **extra_fields: Field tambahan (phone_number, address, dll)

        Returns:
            Tuple[User, error_message]: User object dan error message (jika ada)
        """
        try:
            # Validasi role
            valid_roles = ['ADMIN', 'TEACHER', 'STUDENT', 'PARENT']
            if role not in valid_roles:
                return None, f"Role tidak valid. Pilih dari: {', '.join(valid_roles)}"

            # Check email sudah ada
            if User.objects.filter(email=email).exists():
                return None, "Email sudah terdaftar."

            # Create user
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    role=role,
                    **extra_fields
                )

                # Create token untuk user
                Token.objects.create(user=user)

            return user, None

        except Exception as e:
            return None, f"Error membuat user: {str(e)}"

    @staticmethod
    def update_user(
        user_id: int,
        **fields
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Update data user.

        Args:
            user_id: ID user yang akan diupdate
            **fields: Field yang akan diupdate

        Returns:
            Tuple[User, error_message]: User object dan error message (jika ada)
        """
        try:
            user = User.objects.get(id=user_id)

            # Update password jika ada
            if 'password' in fields:
                user.set_password(fields.pop('password'))

            # Update fields lainnya
            for field, value in fields.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            user.save()
            return user, None

        except User.DoesNotExist:
            return None, "User tidak ditemukan."
        except Exception as e:
            return None, f"Error update user: {str(e)}"

    @staticmethod
    def delete_user(user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Soft delete user (set is_active = False).

        Args:
            user_id: ID user yang akan dihapus

        Returns:
            Tuple[success, error_message]: Status dan error message (jika ada)
        """
        try:
            user = User.objects.get(id=user_id)

            # Soft delete
            user.is_active = False
            user.save()

            # Hapus token
            Token.objects.filter(user=user).delete()

            return True, None

        except User.DoesNotExist:
            return False, "User tidak ditemukan."
        except Exception as e:
            return False, f"Error menghapus user: {str(e)}"

    @staticmethod
    def permanent_delete_user(user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Permanent delete user dari database.

        Args:
            user_id: ID user yang akan dihapus permanent

        Returns:
            Tuple[success, error_message]: Status dan error message (jika ada)
        """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True, None

        except User.DoesNotExist:
            return False, "User tidak ditemukan."
        except Exception as e:
            return False, f"Error menghapus user: {str(e)}"

    @staticmethod
    def login_user(
        email: str,
        password: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Login user dan return token.

        Args:
            email: Email user
            password: Password user

        Returns:
            Tuple[user_data, error_message]: User data dengan token dan error message
        """
        try:
            # Authenticate user
            user = authenticate(username=email, password=password)

            if user is None:
                return None, "Email atau password salah."

            if not user.is_active:
                return None, "Akun tidak aktif."

            # Get or create token
            token, created = Token.objects.get_or_create(user=user)

            # Update last login
            user.save(update_fields=['last_login'])

            # Prepare user data
            user_data = {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
                'role_display': user.get_role_display(),
                'token': token.key,
                'is_verified': user.is_verified,
            }

            return user_data, None

        except Exception as e:
            return None, f"Error login: {str(e)}"

    @staticmethod
    def logout_user(token_key: str) -> Tuple[bool, Optional[str]]:
        """
        Logout user dengan menghapus token.

        Args:
            token_key: Token key user

        Returns:
            Tuple[success, error_message]: Status dan error message (jika ada)
        """
        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return True, None

        except Token.DoesNotExist:
            return False, "Token tidak valid."
        except Exception as e:
            return False, f"Error logout: {str(e)}"

    @staticmethod
    def change_password(
        user_id: int,
        old_password: str,
        new_password: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Ganti password user.

        Args:
            user_id: ID user
            old_password: Password lama
            new_password: Password baru

        Returns:
            Tuple[success, error_message]: Status dan error message (jika ada)
        """
        try:
            user = User.objects.get(id=user_id)

            # Validasi password lama
            if not user.check_password(old_password):
                return False, "Password lama salah."

            # Set password baru
            user.set_password(new_password)
            user.save()

            # Regenerate token
            Token.objects.filter(user=user).delete()
            Token.objects.create(user=user)

            return True, None

        except User.DoesNotExist:
            return False, "User tidak ditemukan."
        except Exception as e:
            return False, f"Error ganti password: {str(e)}"

    @staticmethod
    def reset_password(
        user_id: int,
        new_password: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Reset password user (untuk admin).

        Args:
            user_id: ID user
            new_password: Password baru

        Returns:
            Tuple[success, error_message]: Status dan error message (jika ada)
        """
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            # Regenerate token
            Token.objects.filter(user=user).delete()
            Token.objects.create(user=user)

            return True, None

        except User.DoesNotExist:
            return False, "User tidak ditemukan."
        except Exception as e:
            return False, f"Error reset password: {str(e)}"

    @staticmethod
    def get_user_by_token(token_key: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Get user dari token.

        Args:
            token_key: Token key

        Returns:
            Tuple[User, error_message]: User object dan error message (jika ada)
        """
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            return token.user, None

        except Token.DoesNotExist:
            return None, "Token tidak valid."
        except Exception as e:
            return None, f"Error get user: {str(e)}"

    @staticmethod
    def verify_user(user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Verifikasi user (set is_verified = True).

        Args:
            user_id: ID user

        Returns:
            Tuple[success, error_message]: Status dan error message (jika ada)
        """
        try:
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            return True, None

        except User.DoesNotExist:
            return False, "User tidak ditemukan."
        except Exception as e:
            return False, f"Error verifikasi user: {str(e)}"
