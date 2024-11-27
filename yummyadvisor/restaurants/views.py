from rest_framework import generics, permissions, filters
from django_filters import rest_framework as django_filters  # Burada farklı bir isimlendirme kullandık
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import Restaurant, Review, FavoriteRestaurant
from .serializers import RestaurantSerializer, ReviewSerializer,FavoriteRestaurantSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import BasePermission, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from users.permissions import IsAdmin, IsManager, IsModerator
from datetime import time, timezone

# from yummyadvisor.restaurants import serializers




class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_manager:
            return Restaurant.objects.filter(owner=self.request.user)
        return Restaurant.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all().order_by('id')
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_authenticated and not self.request.user.is_admin:
            return Restaurant.objects.filter(owner=self.request.user).order_by('id')
        return Restaurant.objects.all().order_by('id')


class RestaurantFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')  # Minimum rating filter
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')  # Maximum rating filter
    location_contains = django_filters.CharFilter(field_name='location', lookup_expr='icontains')  # Location search

    class Meta:
        model = Restaurant
        fields = ['category__name', 'min_rating', 'max_rating', 'location_contains']

class RestaurantListView(generics.ListAPIView):
    
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RestaurantFilter  # Yeni eklediğimiz filtre seti burada kullanılıyor
    search_fields = ['name', 'description']
    ordering_fields = ['rating', 'name']

    # Önbellekleme süresini 30 dakikaya çıkartmak için
    @method_decorator(cache_page(60 * 30))  # 30 dakika cache
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        current_time = timezone.now().time()
        return Restaurant.objects.filter(
            opening_time__lte=current_time,
            closing_time__gte=current_time
        ).select_related('category').prefetch_related('reviews').order_by('id')

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    #queryset = Restaurant.objects.prefetch_related('reviews').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user and not self.request.user.is_admin:
            raise PermissionDenied("You do not have permission to edit this review.")
        serializer.save()

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.prefetch_related('restaurant').all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [permissions.AllowAny()]

    # bURRAYI DEPLOYMENT KISMINDA AÇIP REDİS SERVERİ KONTROL ETMEK GEREKİYOR
    # @method_decorator(cache_page(60 * 5))
    # @ratelimit(key='user_or_ip', rate='10/m', block=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        if not restaurant_id:
            raise serializers.ValidationError({"error": "Restaurant ID is required."})

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid Restaurant ID."})

        # Review oluştururken user ve restaurant bilgilerini ekleyin
        serializer.save(user=self.request.user, restaurant=restaurant)
        restaurant.update_rating()  # Restoranın değerlendirme puanını güncelleyin




class ReviewLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @ratelimit(key='user_or_ip', rate='10/m', block=True)
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.likes += 1
        review.save()
        return Response({"message": "Review liked successfully", "likes": review.likes}, status=status.HTTP_200_OK)

class FavoriteRestaurantView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite, created = FavoriteRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)
        if created:
            return Response({"message": f"{restaurant.name} added to your favorites."}, status=status.HTTP_201_CREATED)
        return Response({"message": f"{restaurant.name} is already in your favorites."}, status=status.HTTP_200_OK)

    def delete(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite = FavoriteRestaurant.objects.filter(user=request.user, restaurant=restaurant)
        if favorite.exists():
            favorite.delete()
            return Response({"message": f"{restaurant.name} removed from your favorites."}, status=status.HTTP_200_OK)
        return Response({"error": f"{restaurant.name} is not in your favorites."}, status=status.HTTP_400_BAD_REQUEST)


class TopReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Review.objects.filter(restaurant_id=restaurant_id).order_by('-likes')[:5]  # En çok beğenilen 5 yorumu getirir

class AdvancedRestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all().select_related('category').prefetch_related('reviews').order_by('id')
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'rating', 'location']
    search_fields = ['name', 'description']
    ordering_fields = ['rating', 'name', 'location']

class ReviewModerationView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(approved=True)

class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_moderator)

class FavoriteRestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteRestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteRestaurant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        restaurant = self.request.data.get('restaurant')
        if not restaurant:
            raise serializers.ValidationError({"error": "Restaurant ID is required"})
        serializer.save(user=self.request.user)

class FavoriteRestaurantDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteRestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteRestaurant.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        favorite = get_object_or_404(FavoriteRestaurant, pk=kwargs['pk'], user=request.user)
        favorite.delete()
        return Response({"message": "Favorite restaurant removed"}, status=status.HTTP_200_OK)