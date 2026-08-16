from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class CookieJWTAuthentication(BaseAuthentication):
    """Authentifie via JWT dans les cookies HttpOnly"""
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None  # Pas de cookie, passer au suivant
        
        from rest_framework_simplejwt.authentication import JWTAuthentication
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            # Récupérer l'utilisateur depuis le modèle personnalisé
            user_id = validated_token.get('user_id')
            user = User.objects.get(user_id=user_id)
            # Garantir que l'objet user présente l'attribut attendu par Django
            if not hasattr(user, 'is_authenticated'):
                # Ajouter un attribut booléen simple pour satisfaire les checks DRF
                user.is_authenticated = True
            return (user, validated_token)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
