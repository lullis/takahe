from django.db import models


class ListingType(models.TextChoices):
    All = "All"
    Local = "Local"
    Subscribed = "Subscribed"
    ModeratorView = "ModeratorView"


class RegistrationMode(models.TextChoices):
    Closed = "Closed"
    RequireApplication = "RequireApplication"
    Open = "Open"


class SortType(models.TextChoices):
    Active = "Active"
    Hot = "Hot"
    New = "New"
    Old = "Old"
    TopDay = "TopDay"
    TopWeek = "TopWeek"
    TopMonth = "TopMonth"
    TopYear = "TopYear"
    TopAll = "TopAll"
    MostComments = "MostComments"
    NewComments = "NewComments"
    TopHour = "TopHour"
    TopSixHour = "TopSixHour"
    TopTwelveHour = "TopTwelveHour"
    TopThreeMonths = "TopThreeMonths"
    TopSixMonths = "TopSixMonths"
    TopNineMonths = "TopNineMonths"
    Controversial = "Controversial"
    Scaled = "Scaled"


class PostListingMode(models.TextChoices):
    List = "List"
    Card = "Card"
    SmallCard = "SmallCard"


class ModlogActionType(models.TextChoices):
    All = "All"
    ModRemovePost = "ModRemovePost"
    ModLockPost = "ModLockPost"
    ModFeaturePost = "ModFeaturePost"
    ModRemoveComment = "ModRemoveComment"
    ModRemoveCommunity = "ModRemoveCommunity"
    ModBanFromCommunity = "ModBanFromCommunity"
    ModAddCommunity = "ModAddCommunity"
    ModTransferCommunity = "ModTransferCommunity"
    ModAdd = "ModAdd"
    ModBan = "ModBan"
    ModHideCommunity = "ModHideCommunity"
    AdminPurgePerson = "AdminPurgePerson"
    AdminPurgeCommunity = "AdminPurgeCommunity"
    AdminPurgePost = "AdminPurgePost"
    AdminPurgeComment = "AdminPurgeComment"


class SearchType(models.TextChoices):
    All = "All"
    Comments = "Comments"
    Posts = "Posts"
    Communities = "Communities"
    Users = "Users"
    Url = "Url"


class SubscribedType(models.TextChoices):
    Subscribed = "Subscribed"
    NotSubscribed = "NotSubscribed"
    Pending = "Pending"


class PostFeatureType(models.TextChoices):
    Local = "Local"
    Community = "Community"


class CommentSortType(models.TextChoices):
    Hot = "Hot"
    Top = "Top"
    New = "New"
    Old = "Old"
    Controversial = "Controversial"
