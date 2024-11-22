from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter  # Burada içe aktarımı ekledik
from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    Kategorileri listeleyen ve adminlerin yeni kategori oluşturmasını sağlayan API.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]  # Arama filtresi özelliği ekleniyor
    search_fields = ['name', 'description']  # Aranabilir alanlar

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Kategorilerin detayını görüntüleme, güncelleme veya silme işlemleri.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
