import logging

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ArticleNotFound
from .models import Article, ArticleViews
from .pagination import ArticlePagination
from .serializers import (ArticleCreateSerializer, ArticleSerializer,
                          ArticleViewSerializer)

# Create your views here.

logger = logging.getLogger(__name__)


class ArticleFilter(django_filters.FilterSet):

    advert_type = django_filters.CharFilter(
        field_name="advert_type", lookup_expr="iexact"
    )

    article_type = django_filters.CharFilter(
        field_name="article_type", lookup_expr="iexact"
    )

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Article
        fields = ["advert_type", "article_type", "price"]


class ListAllArticlesAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("-created_at")
    pagination_class = ArticlePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ArticleFilter
    search_fields = ["country"]
    ordering_fields = ["created_at"]


class ListAuthorsArticleAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("-created_at")
    pagination_class = ArticlePagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ArticleFilter
    search_fields = ["country"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.filter(user=user).order_by("-created_at")

        return queryset


class ArticleViewsAPIView(generics.ListAPIView):
    serializer_class = ArticleViewSerializer
    queryset = ArticleViews.objects.all()


class ArticleDetailView(APIView):
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not ArticleViews.objects.filter(article=article, ip=ip).exists():

            ArticleViews.objects.create(article=article, ip=ip)

            article.views += 1
            article.save()

        serializer = ArticleSerializer(article, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_article_api_view(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise ArticleNotFound

    user = request.user
    if article.user != user:
        return Response(
            {"error": "You can't update or edit an article doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "PUT":
        data = request.data
        serializer = ArticleSerializer(article, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_article_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    serializer = ArticleCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"article {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_article_api_view(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise ArticleNotFound

    user = request.user
    if article.user != user:
        return Response(
            {"error": "You can't update or edit an article doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = article.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion Failed"

        return Response(data=data)


@api_view(["POST"])
def uploadArticleImage(request):
    data = request.data
    article_id = data["article_id"]
    article = Article.objects.get(id=article_id)
    article.cover_photo = request.FILES.get("cover_photo")
    article.photo1 = request.FILES.get("photo1")
    article.photo2 = request.FILES.get("photo2")
    article.photo3 = request.FILES.get("photo3")
    article.photo4 = request.FILES.get("photo4")

    article.save()

    return Response("Image(s) Uploaded!")


class ArticleSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleCreateSerializer

    def post(self, request):
        queryset = Article.objects.filter(published_status=True)
        data = self.request.data

        advert_type = data["advert_type"]
        queryset = queryset.filter(advert_type__iexact=advert_type)

        article_type = data["article_type"]
        queryset = queryset.filter(article_type__iexact=article_type)

        price = data["price"]
        if price == "€0+":
            price = 0
        elif price == "€50,00+":
            price = 50
        elif price == "€100,00+":
            price = 100
        elif price == "€150,00+":
            price = 150
        elif price == "€200,00+":
            price = 200
        elif price == "€250,00+":
            price = 250
        elif price == "€300,00+":
            price = 300
        elif price == "€350,00+":
            price = 350
        elif price == "€400,00+":
            price = 400
        elif price == "€450,00+":
            price = 450
        elif price == "€500,00+":
            price = 500
        elif price == "Any":
            price = -1

        if price != -1:
            queryset = queryset.filter(price__gte=price)

        total_words = data["total_words"]
        if total_words == "0+":
            total_words = 0
        elif total_words == "10+":
            total_words = 10
        elif total_words == "100+":
            total_words = 100
        elif total_words == "150+":
            total_words = 150
        elif total_words == "200+":
            total_words = 200
        elif total_words == "250+":
            total_words = 250
        elif total_words == "300+":
            total_words = 300
        elif total_words == "350+":
            total_words = 350
        elif total_words == "400+":
            total_words = 400
        elif total_words == "450+":
            total_words = 450
        elif total_words == "500+":
            total_words = 500

        queryset = queryset.filter(total_words__gte=total_words)

        paragraphs = data["paragraphs"]
        if paragraphs == "0+":
            paragraphs = 0
        elif paragraphs == "1+":
            paragraphs = 1
        elif paragraphs == "2+":
            paragraphs = 2
        elif paragraphs == "3+":
            paragraphs = 3
        elif paragraphs == "4+":
            paragraphs = 4
        elif paragraphs == "5+":
            paragraphs = 5
        elif paragraphs == "6+":
            paragraphs = 6
        elif paragraphs == "7+":
            paragraphs = 7
        elif paragraphs == "8+":
            paragraphs = 8
        elif paragraphs == "9+":
            paragraphs = 9
        elif paragraphs == "10+":
            paragraphs = 10

        queryset = queryset.filter(paragraphs__gte=paragraphs)

        subtitles = data["subtitles"]
        if subtitles == "0+":
            subtitles = 0
        elif subtitles == "1+":
            subtitles = 1
        elif subtitles == "2+":
            subtitles = 2
        elif subtitles == "3+":
            subtitles = 3
        elif subtitles == "4+":
            subtitles = 4
        elif subtitles == "5+":
            subtitles = 5
        elif subtitles == "6+":
            subtitles = 6
        elif subtitles == "7+":
            subtitles = 7
        elif subtitles == "8+":
            subtitles = 8
        elif subtitles == "9+":
            subtitles = 9
        elif subtitles == "10+":
            subtitles = 10

        queryset = queryset.filter(subtitles__gte=subtitles)

        keywords = data["keywords"]
        if keywords == "0+":
            keywords = 0
        elif keywords == "1+":
            keywords = 1
        elif keywords == "2+":
            keywords = 2
        elif keywords == "3+":
            keywords = 3
        elif keywords == "4+":
            keywords = 4
        elif keywords == "5+":
            keywords = 5
        elif keywords == "6+":
            keywords = 6
        elif keywords == "7+":
            keywords = 7
        elif keywords == "8+":
            keywords = 8
        elif keywords == "9+":
            keywords = 9
        elif keywords == "10+":
            keywords = 10

        queryset = queryset.filter(keywords__gte=keywords)

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = ArticleSerializer(queryset, many=True)

        return Response(serializer.data)
