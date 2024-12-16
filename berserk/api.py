from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from berserk.models import BerserkCharacter, BerserkCreature, BerserkGeography, BerserkArmy, BerserkArtifact, Album

from berserk.serializers import BerserkCharacterSerializer, BerserkCreatureSerializer, BerserkGeographySerializer, BerserkArmySerializer, BerserkArtifactSerializer, AlbumSerializer, UserSerializer

from berserk.serializers import BerserkCharacterCreateSerializer, BerserkArmyCreateSerializer, BerserkCreatureCreateSerializer, BerserkArtifactCreateSerializer, BerserkGeographyCreateSerializer, AlbumCreateSerializer
from django.db.models import Avg, Count, Max, Min, Case, When, Sum, Q, Subquery, OuterRef
from rest_framework import serializers

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({'success': True})
    else:
        return Response({'success': False, 'error': 'Неверный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_view(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        # email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'success': False, 'error': 'Имя пользователя уже занято'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)  #, email=email)
        user.save()

        login(request, user)

        return Response({'success': True, 'message': 'Регистрация прошла успешно'})

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet( mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserProfileViewSet(GenericViewSet):
    @action(detail=False, methods=['get'], url_path='info')
    def get_info(self, request, *args, **kwargs):

        #user = request.User
        data = {
            "is_authenticated": self.request.user.is_authenticated
        }
        if self.request.user.is_authenticated:
            data.update({
                "is_superuser":self.request.user.is_superuser,
                "name": self.request.user.username
            })
        return Response(data)
        #return Response({
           # "is_superuser": self.request.user.is_superuser,
           # "is_authenticated": self.request.user.is_authenticated
        #})
    
    permission_classes = [IsAuthenticated]

    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class OTPRequired(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and cache.get('otp_good', False))
        
    @action(detail=False, url_path="check-login", methods=['GET'], permission_classes=[])
    def get_check_login(self, request, *args, **kwargs):
        return Response({
            'is_authenticated': self.request.user.is_authenticated
        })
    
    @action(detail=False, url_path="login", methods=['GET'], permission_classes=[])
    def use_login(self, request, *args, **kwargs):
        user= authenticate(username='username', password='pass')
        if user:
            login(request, user)
        return Response({
            'is_authenticated': bool(user)
        })

    @action(detail=False, url_path='otp-login', methods=['POST'], serializer_class=OTPSerializer)
    def otp_login(self, *args, **kwargs):
         # 'otpauth://totp/Maria%20App:maria?secret=JBSWY3DPEHPK3PXP&issuer=Maria%20App'
        # totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')

        # serializer = self.get_serializer(data=self.request.data)
        # serializer.is_valid(raise_exception=True)

        # success = False
        # if totp.verify(serializer.validated_data['key']):
        #     cache.set('otp_good', True, 10)
        #     success = True
        cache.set('otp_good', True, 300)
        success = True

        return Response({
            'success': success
        })
    
    @action(detail=False, methods=['GET'], url_path='otp-status')
    def get_otp_status(self, *args, **kwargs):
        otp_good = cache.get('otp_good', False)
        return Response({
            'otp_good': otp_good
        })
    
    @action(detail=False, url_path='otp-required', permission_classes=[OTPRequired])
    def page_with_otp_required(self, *args, **kwargs):
        return Response({
            'success': True
        })

class BerserkCharacterViewSet(
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin, 
    GenericViewSet
 ):
    queryset = BerserkCharacter.objects.all()
    serializer_class = BerserkCharacterSerializer
   
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                qs = qs.filter(user=self.request.user)
        else:
            qs = BerserkCharacter.objects.none()
        return qs

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BerserkCharacterCreateSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы для выполнения этого действия.")
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request):

        selected_user_id = request.GET.get('selectedUserId')
        selected_creature_id = request.GET.get('selectedCreatureId')
        selected_army_id = request.GET.get('selectedArmyId')
        is_with_picture = request.GET.get('isWithPicture')
        is_without_picture = request.GET.get('isWithoutPicture')

        queryset = self.get_queryset()

        if selected_user_id:
            queryset = queryset.filter(user=selected_user_id)
        if selected_creature_id:
            queryset = queryset.filter(creature__id=selected_creature_id)
        if selected_army_id:
            queryset = queryset.filter(army__id=selected_army_id)
        if is_with_picture == 'true':
            queryset = queryset.filter(picture__isnull=False)
        if is_without_picture == 'true':
            queryset = queryset.filter(picture__isnull=True)

        df = pd.DataFrame(queryset.values())
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=berserk_characters.xlsx'
        df.to_excel(response, index=False)
        return response
    
    @action (detail=False, methods=["GET"], url_path="stats") 
    def get_stats (self, request, *args, **kwargs):
        class StatsSerializer(serializers.Serializer):
            count=serializers.IntegerField()
            count_with_image=serializers.IntegerField()
            avg=serializers.IntegerField()
            max=serializers.IntegerField()
            min=serializers.IntegerField()
            most_common_creature = serializers.ListField(
                child=serializers.CharField(),
                required=False
            ) 
            class Meta:
                fields = '__all__'
        # Общие статистики
        # Общие статистики
        user = request.query_params.get('user')
        creature = request.query_params.get('creature')
        army = request.query_params.get('army')
        with_picture = request.query_params.get('with_picture')
        without_picture = request.query_params.get('without_picture')
        queryset = BerserkCharacter.objects.all()
        if user:
            queryset = queryset.filter(user=user)
        if creature:
            queryset = queryset.filter(creature=creature)
        if army:
            queryset = queryset.filter(army=army)
        if with_picture:
            queryset = queryset.exclude(picture='')
        if without_picture:
            queryset = queryset.filter(picture='')        

        general_stats = queryset.aggregate(
            count=Count("*"),
            count_with_image=Sum(Case(When(Q(picture=''), then=0), default=1)),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id"),
        )

        # Получаем creature_id с максимальным количеством вхождений
        max_count_creature_ids = queryset.values('creature_id') \
            .annotate(count=Count('creature_id')) \
            .order_by('-count')

        if max_count_creature_ids:
            max_count = max_count_creature_ids[0]['count']
            max_count_creature_ids = max_count_creature_ids.filter(count=max_count).values_list('creature_id', flat=True)

            most_common_creature = BerserkCreature.objects.filter(id__in=max_count_creature_ids) \
                .annotate(
                    count=Subquery(
                        BerserkCharacter.objects.filter(creature_id=OuterRef('id'))
                        .values('creature_id')
                        .annotate(count=Count('creature_id'))
                        .values('count')
                    )
                ) \
                .values('name', 'count')

            # Объединяем данные
            data = {
                **general_stats,
                'most_common_creature': [creature['name'] for creature in most_common_creature]
            }
        else:
            data = {
                **general_stats,
                'most_common_creature': None
            }
    
        serializer = StatsSerializer(instance=data)
        return Response(serializer.data) 

class BerserkCreatureViewSet( mixins.DestroyModelMixin, 
                             mixins.RetrieveModelMixin, 
                             mixins.UpdateModelMixin,
                             mixins.CreateModelMixin, 
                             mixins.ListModelMixin, 
                             GenericViewSet):
    queryset = BerserkCreature.objects.all()
    serializer_class = BerserkCreatureSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BerserkCreatureCreateSerializer
        return super().get_serializer_class()

class BerserkGeographyViewSet(mixins.DestroyModelMixin, 
                              mixins.RetrieveModelMixin, 
                              mixins.UpdateModelMixin, 
                              mixins.CreateModelMixin, 
                              mixins.ListModelMixin, 
                              GenericViewSet):
    queryset = BerserkGeography.objects.all()
    serializer_class = BerserkGeographySerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BerserkGeographyCreateSerializer
        return super().get_serializer_class()

class BerserkArmyViewSet(mixins.DestroyModelMixin, 
                         mixins.RetrieveModelMixin, 
                         mixins.UpdateModelMixin, 
                         mixins.CreateModelMixin, 
                         mixins.ListModelMixin, 
                         GenericViewSet):
    queryset = BerserkArmy.objects.all()
    serializer_class = BerserkArmySerializer    

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BerserkArmyCreateSerializer
        return super().get_serializer_class()

class BerserkArtifactViewSet(mixins.DestroyModelMixin, 
                             mixins.RetrieveModelMixin, 
                             mixins.UpdateModelMixin, 
                             mixins.CreateModelMixin, 
                             mixins.ListModelMixin, 
                             GenericViewSet):
    queryset = BerserkArtifact.objects.all()
    serializer_class = BerserkArtifactSerializer    

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BerserkArtifactCreateSerializer
        return super().get_serializer_class()
    
class AlbumViewSet(mixins.DestroyModelMixin, 
                             mixins.RetrieveModelMixin, 
                             mixins.UpdateModelMixin, 
                             mixins.CreateModelMixin, 
                             mixins.ListModelMixin, 
                             GenericViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer    

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return AlbumCreateSerializer
        return super().get_serializer_class()    
