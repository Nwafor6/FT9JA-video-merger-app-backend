from .models import ShortLink

def generate_short_url(link):
    shortlink=ShortLink.objects.create(
        original_url=link
    )
    return shortlink.short_url