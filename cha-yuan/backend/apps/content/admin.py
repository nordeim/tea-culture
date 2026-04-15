"""
Django Admin Configuration for Content Models

Custom admin interfaces for Article and ArticleCategory.
Includes rich text editing and publishing workflows.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "article_count", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]

    def article_count(self, obj):
        return obj.articles.count()

    article_count.short_description = "Articles"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "is_published_display",
        "is_featured",
        "reading_time_minutes",
        "published_at",
        "created_at",
    ]
    list_filter = [
        "is_featured",
        "category",
        "published_at",
        "created_at",
    ]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]

    fieldsets = (
        (
            "Content",
            {
                "fields": ("title", "slug", "category", "content", "excerpt"),
            },
        ),
        (
            "Publishing",
            {
                "fields": ("published_at", "is_featured"),
                "classes": ("collapse",),
            },
        ),
        (
            "Media & SEO",
            {
                "fields": ("featured_image", "meta_description"),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("reading_time_minutes", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at", "reading_time_minutes"]

    actions = ["publish_selected", "unpublish_selected", "make_featured"]

    def is_published_display(self, obj):
        if obj.is_published:
            return format_html('<span style="color: #5C8A4D;">● Published</span>')
        return format_html('<span style="color: #999;">○ Draft</span>')

    is_published_display.short_description = "Status"

    def publish_selected(self, request, queryset):
        from django.utils import timezone

        queryset.update(published_at=timezone.now())

    publish_selected.short_description = "Publish selected articles"

    def unpublish_selected(self, request, queryset):
        queryset.update(published_at=None)

    unpublish_selected.short_description = "Unpublish selected articles"

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    make_featured.short_description = "Mark as featured"
