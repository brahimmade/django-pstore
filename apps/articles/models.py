import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedUUIDModel

# Create your models here.

User = get_user_model()


class ArticlePublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(ArticlePublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )


class Article(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_READ = "For Read", _("For Read")
        AUCTION = "Auction", _("Auction")

    class ArticleType(models.TextChoices):
        BOOK_REVIEW = "Book Review", _("Book Review")
        SHORT_REPORT = "Short Report", _("Short Report")
        SOFTWARE_ARTICLE = "Software Article", _("Software Article")
        NEWS_ARTICLE = "News Article", _("News Article")
        RESEARCH_ARTICLE = "Research Article", _("Research Article")
        REVIEW_ARTICLE = "Review Article", _("Review Article")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(User, verbose_name=_("Author, Seller or Buyer"), related_name="author_buyer", on_delete=models.DO_NOTHING)
    title = models.CharField(verbose_name=_("Article Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(verbose_name=_("Article Reference Code"), max_length=255, unique=True, blank=True)
    description = models.CharField(verbose_name=_("Description"), default="Default description...update me please....", max_length=255)
    country = CountryField(verbose_name=_("Country"), default="GR", blank_label="(select country)")
    article_number = models.IntegerField(verbose_name=_("Article Number"), validators=[MinValueValidator(1)], default=112)
    price = models.DecimalField(verbose_name=_("Price"), max_digits=6, decimal_places=2, default=0.0)
    tax = models.DecimalField(verbose_name=_("Article Tax"), max_digits=6, decimal_places=2, default=0.24, help_text="24% article tax charged")
    words = models.IntegerField(verbose_name=_("Number of Words"), default=0)
    total_words = models.IntegerField(verbose_name=_("Total Number of Words"), default=0)
    paragraphs = models.IntegerField(verbose_name=_("Paragraphs"), default=0)
    subtitles = models.IntegerField(verbose_name=_("Subtitles"), default=0)
    keywords = models.IntegerField(verbose_name=_("Keywords"), blank=True, null=True, default=0)
    advert_type = models.CharField(verbose_name=_("Advert Type"), max_length=50, choices=AdvertType.choices, default=AdvertType.FOR_SALE)
    article_type = models.CharField(verbose_name=_("Article Type"), max_length=50, choices=ArticleType.choices, default=ArticleType.OTHER)
    cover_photo = models.ImageField(verbose_name=_("Article Cover"), default="/article_sample.png", null=True, blank=True)
    photo1 = models.ImageField(default="/interior_sample.png", null=True, blank=True)
    photo2 = models.ImageField(default="/interior_sample.png", null=True, blank=True)
    photo3 = models.ImageField(default="/interior_sample.png", null=True, blank=True)
    photo4 = models.ImageField(default="/interior_sample.png", null=True, blank=True)
    published_status = models.BooleanField(verbose_name=_("Published Status"), default=False)
    views = models.ImageField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()
    published = ArticlePublishedManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.description(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )

        super(Article, self).save(*args, **kwargs)

    @property
    def final_article_title(self):
        tax_percentage = self.tax
        article_price = self.price
        tax_ammount = round(tax_percentage * article_price, 2)
        price_after_tax = float(round(article_price + tax_ammount, 2))
        return price_after_tax


class ArticleViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    article = models.ForeignKey(Article, related_name="article_views", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (
            f"Total views on - {self.article.title} is - {self.article.views} view(s)"
        )

    class Meta:
        verbose_name = 'Total Views on Article'
        verbose_name_plural = 'Total Articles Views'
