from django.db import models

class Quote(models.Model):
    text = models.CharField(max_length=256, unique=True)
    source = models.CharField(max_length=48)
    source_type = models.CharField(max_length=16)
    weight = models.IntegerField()
    views = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)

async def acreate_quote(text, source, source_type, weight):
    quote = await Quote.objects.acreate(text=text, source=source, source_type=source_type, weight=weight)
    return quote
