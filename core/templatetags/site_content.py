"""Template tags for editable page text (see the SiteContent model).

The whole table is loaded once per process and cached; the cache is cleared
whenever a SiteContent row is saved or deleted.
"""

from django import template
from django.db.models.signals import post_delete, post_save
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_cache = None


def _contents():
    """Return {key: SiteContent}, loading the table on first use."""
    global _cache
    if _cache is None:
        from core.models import SiteContent

        try:
            _cache = {item.key: item for item in SiteContent.objects.all()}
        except Exception:
            # Table may not exist yet (e.g. before the first migrate).
            _cache = {}
    return _cache


def _clear_cache(**kwargs):
    global _cache
    _cache = None


post_save.connect(_clear_cache, dispatch_uid="core.site_content.save")
post_delete.connect(_clear_cache, dispatch_uid="core.site_content.delete")


def _value(key, default):
    item = _contents().get(key)
    if item and item.value:
        return item.value
    return default


@register.simple_tag
def site_text(key, default=""):
    """Plain text, escaped by the template engine."""
    return _value(key, default)


@register.simple_tag
def site_html(key, default=""):
    """Text rendered as-is; use for values flagged is_html (trusted staff only)."""
    return mark_safe(_value(key, default))


@register.simple_tag
def site_paragraphs(key, default=""):
    """Text where blank lines separate paragraphs; returns ready-made <p> tags."""
    value = _value(key, default)
    chunks = [chunk.strip() for chunk in value.split("\n\n") if chunk.strip()]
    return mark_safe("".join(f"<p>{escape(chunk)}</p>" for chunk in chunks))
