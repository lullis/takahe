from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.Site)
def on_site_created_maybe_create_local_site(sender, **kw):
    site = kw["instance"]
    created = kw["created"]

    if created and site.local:
        models.LocalSite.objects.create(site=site)


@receiver(post_save, sender=models.Site)
def on_site_created_maybe_create_aggregates(sender, **kw):
    site = kw["instance"]
    if kw["created"]:
        models.SiteAggregates.objects.create(site=site)


@receiver(post_save, sender=models.Person)
def on_person_created_maybe_create_aggregates(sender, **kw):
    person = kw["instance"]
    if kw["created"]:
        models.PersonAggregates.objects.create(person=person)
