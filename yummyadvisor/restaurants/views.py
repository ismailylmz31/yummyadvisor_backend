from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import Restaurant, Review,FavoriteRestaurant
from .serializers import RestaurantSerializer, ReviewSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrAdmin]

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all().select_related('category').prefetch_related('reviews')
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'rating', 'location']
    search_fields = ['name', 'description']
    ordering_fields = ['rating', 'name']

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user and not self.request.user.is_admin:
            raise PermissionDenied("You do not have permission to edit this review.")
        serializer.save()

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @ratelimit(key='user', rate='3/m', block=True)  # Kullanıcı başına dakika başına 3 istek sınırı
    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        review.restaurant.update_rating()  # Restoran puanını güncellemek için çağrı

class ReviewLikeView(APIView):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.likes += 1
        review.save()
        return Response({"message": "Review liked successfully", "likes": review.likes}, status=status.HTTP_200_OK)



class FavoriteRestaurantView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite, created = FavoriteRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)
        if created:
            return Response({"message": "Restaurant added to favorites"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Restaurant is already in your favorites"}, status=status.HTTP_200_OK)

    def delete(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite = FavoriteRestaurant.objects.filter(user=request.user, restaurant=restaurant)
        if favorite.exists():
            favorite.delete()
            return Response({"message": "Restaurant removed from favorites"}, status=status.HTTP_200_OK)
        return Response({"message": "Restaurant is not in your favorites"}, status=status.HTTP_400_BAD_REQUEST)
    

class TopReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Review.objects.filter(restaurant_id=restaurant_id).order_by('-likes')[:5]  # En çok beğenilen 5 yorumu getirir    