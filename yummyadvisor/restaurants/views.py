from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import Restaurant, Review
from .serializers import RestaurantSerializer, ReviewSerializer
from rest_framework.exceptions import PermissionDenied

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
