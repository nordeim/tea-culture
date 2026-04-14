"""
Commerce models for CHA YUAN - Product catalog with Singapore GST pricing.
"""

from decimal import Decimal, ROUND_HALF_UP

from django.db import models

from apps.core.models import User


class Origin(models.Model):
    """Tea origin region."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "origins"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.region})"


class TeaCategory(models.Model):
    """Tea category with fermentation level and brewing guide."""

    FERMENTATION_CHOICES = [
        (0, "White Tea (0%)"),
        (5, "Green Tea (0-5%)"),
        (45, "Oolong Tea (15-70%)"),
        (100, "Black Tea (100%)"),
        (-1, "Pu'erh Tea (Post-fermented)"),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    fermentation_level = models.IntegerField(
        choices=FERMENTATION_CHOICES,
        help_text="Oxidation percentage",
    )
    description = models.TextField()
    brewing_temp_celsius = models.IntegerField(
        help_text="Recommended brewing temperature in Celsius",
    )
    brewing_time_seconds = models.IntegerField(
        help_text="Recommended brewing time in seconds",
    )
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tea_categories"
        verbose_name_plural = "tea categories"
        ordering = ["fermentation_level"]

    def __str__(self):
        return self.name

    def get_brewing_temp_display(self):
        """Return brewing temperature with unit."""
        return f"{self.brewing_temp_celsius}°C"

    def get_brewing_time_display(self):
        """Return brewing time in minutes/seconds format."""
        if self.brewing_time_seconds >= 60:
            minutes = self.brewing_time_seconds // 60
            seconds = self.brewing_time_seconds % 60
            if seconds > 0:
                return f"{minutes}:{seconds:02d} min"
            return f"{minutes} min"
        return f"{self.brewing_time_seconds} sec"


class Product(models.Model):
    """Tea product with Singapore GST pricing."""

    SEASON_CHOICES = [
        ("spring", "Spring"),
        ("summer", "Summer"),
        ("autumn", "Autumn"),
        ("winter", "Winter"),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255)

    # Pricing (SGD)
    price_sgd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price in SGD (before GST)",
    )
    gst_inclusive = models.BooleanField(
        default=True,
        help_text="Whether price includes GST",
    )

    # Inventory
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    # Relationships
    origin = models.ForeignKey(
        Origin,
        on_delete=models.CASCADE,
        related_name="products",
    )
    category = models.ForeignKey(
        TeaCategory,
        on_delete=models.CASCADE,
        related_name="products",
    )

    # Tea-specific fields
    harvest_season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        blank=True,
    )
    harvest_year = models.PositiveIntegerField(null=True, blank=True)
    weight_grams = models.PositiveIntegerField(default=50)
    is_new_arrival = models.BooleanField(default=False)
    is_subscription_eligible = models.BooleanField(default=True)

    # Media
    image = models.URLField(blank=True)
    images = models.JSONField(default=list, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["-is_new_arrival", "-created_at"]

    def __str__(self):
        return self.name

    def get_price_with_gst(self):
        """Calculate price with GST included."""
        if self.gst_inclusive:
            return self.price_sgd
        # GST 9%
        gst_rate = Decimal("0.09")
        total = self.price_sgd * (Decimal("1") + gst_rate)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_gst_amount(self):
        """Calculate GST amount."""
        if self.gst_inclusive:
            # Extract GST from inclusive price
            base = self.price_sgd / Decimal("1.09")
            gst = self.price_sgd - base
        else:
            gst = self.price_sgd * Decimal("0.09")
        return gst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock > 0 and self.is_available

    def get_weight_display(self):
        """Return weight with unit."""
        return f"{self.weight_grams}g"

    def get_season_display_with_year(self):
        """Return season and year if available."""
        if self.harvest_season and self.harvest_year:
            return f"{self.get_harvest_season_display()} {self.harvest_year}"
        return self.get_harvest_season_display() if self.harvest_season else ""
