from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from hatchway import ApiResponse, api_view

from .. import models, schemas


def add_admin(request):
    pass


def banned_users(request):
    pass


def block(request):
    pass


def create(request):
    pass


def federated(request):
    pass


def leave_site(request):
    pass


@api_view.get
def site_detail(request: HttpRequest) -> ApiResponse[schemas.GetSiteResponse]:
    site = get_object_or_404(models.Site, domain__default=True)
    site_view = schemas.SiteView(
        site=schemas.Site.from_orm(site),
        local_site=schemas.LocalSite.from_orm(site.localsite),
        local_site_rate_limit=schemas.LocalSiteRateLimit.from_orm(
            site.localsite.localsiteratelimit
        ),
        counts=schemas.SiteAggregates.from_orm(site.siteaggregates),
    )
    admins = [
        schemas.PersonView(
            person=schemas.Person.from_orm(admin),
            counts=schemas.PersonAggregates.from_orm(admin.personaggregates),
            is_admin=True,
        )
        for admin in site.admins.all()
    ]
    instance = models.Instance.objects.get(domain=site.domain)

    return ApiResponse(
        schemas.GetSiteResponse(
            site_view=site_view,
            admins=admins,
            all_languages=[],
            discussion_languages=[],
            taglines=[],
            custom_emojis=[],
            version=instance.version,
        )
    )


def update(request):
    pass
