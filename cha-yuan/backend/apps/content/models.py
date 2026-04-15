"""
Content Models - Tea Culture Articles
Article and ArticleCategory models for tea culture content.
"""

import re
from django.db import models
from django.utils.text import slugify


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#5C8A4D")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    featured_image = models.ImageField(upload_to="articles/", blank=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    reading_time_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.published_at is not None

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = self._generate_unique_slug(base_slug)
        
        if not self.excerpt:
            self.excerpt = self._generate_excerpt()
        
        self.reading_time_minutes = self._calculate_reading_time()
        
        if len(self.meta_description) > 160:
            self.meta_description = self.meta_description[:157] + "..."
        
        super().save(*args, **kwargs)

    def _generate_unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def _generate_excerpt(self):
        plain_text = re.sub(r'[#*_`\[\]\(\)!]', '', self.content)
        plain_text = ' '.join(plain_text.split())
        if len(plain_text) <= 300:
            return plain_text
        return plain_text[:297] + "..."

    def _calculate_reading_time(self):
        plain_text = re.sub(r'[#*_`\[\]\(\)!]', '', self.content)
        word_count = len(plain_text.split())
        return max(1, round(word_count / 200))
