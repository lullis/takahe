from typing import Literal, NewType

SiteId = NewType("SiteId", int)
LocalSiteId = NewType("LocalSiteId", int)
InstanceId = NewType("InstanceId", int)
PersonId = NewType("PersonId", int)
UserId = NewType("UserId", int)
LocalUserId = NewType("LocalUserId", int)
CommunityId = NewType("CommunityId", int)
PostId = NewType("PostId", int)
CustomEmojiId = NewType("CustomEmojiId", int)
CommentId = NewType("CommentId", int)
CommentReplyId = NewType("CommentReplyId", int)
LanguageId = NewType("LanguageId", int)
PostReportId = NewType("PostReportId", int)
ImageUrl = NewType("ImageUrl", str)
ActorId = NewType("ActorId", str)
ActivityId = NewType("ActivityId", int)
ActivityPubInbox = NewType("ActivityPubInbox", str)
PaginationCursor = NewType("PaginationCursor", str)
PersonMentionId = NewType("PersonMentionId", int)
PrivateMessageReportId = NewType("PrivateMessageReportId", int)
PrivateMessageId = NewType("PrivateMessageId", int)
CommentReportId = NewType("CommentReportId", int)

LISTING_TYPES = Literal["All", "Local", "Subscribed", "ModeratorView"]
REGISTRATION_MODE_OPTIONS = Literal["Closed", "RequireApplication", "Open"]
SORT_TYPE_OPTIONS = Literal[
    "Active",
    "Hot",
    "New",
    "Old",
    "TopDay",
    "TopWeek",
    "TopMonth",
    "TopYear",
    "TopAll",
    "MostComments",
    "NewComments",
    "TopHour",
    "TopSixHour",
    "TopTwelveHour",
    "TopThreeMonths",
    "TopSixMonths",
    "TopNineMonths",
    "Controversial",
    "Scaled",
]
POST_LISTING_MODE_OPTIONS = Literal["List", "Card", "SmallCard"]
MOD_LOG_ACTION_TYPES = Literal[
    "All",
    "ModRemovePost",
    "ModLockPost",
    "ModFeaturePost",
    "ModRemoveComment",
    "ModRemoveCommunity",
    "ModBanFromCommunity",
    "ModAddCommunity",
    "ModTransferCommunity",
    "ModAdd",
    "ModBan",
    "ModHideCommunity",
    "AdminPurgePerson",
    "AdminPurgeCommunity",
    "AdminPurgePost",
    "AdminPurgeComment",
]
SEARCH_TYPES = Literal["All", "Comments", "Posts", "Communities", "Users", "Url"]
SUBSCRIPTION_TYPES = Literal["Subscribed", "NotSubscribed", "Pending"]
POST_FEATURE_TYPES = Literal["Local", "Community"]
COMMENT_SORT_TYPES = Literal["Hot", "Top", "New", "Old", "Controversial"]
