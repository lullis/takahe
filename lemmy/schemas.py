from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Extra, Field

from . import types


class ErrorResponseRegistration(BaseModel):
    error: Literal[
        "registration_closed",
        "email_required",
        "registration_application_answer_required",
        "passwords_do_not_match",
        "captcha_incorrect",
        "email_already_exists",
        "user_already_exists",
    ]


class ErrorResponseLogin(BaseModel):
    error: Literal[
        "incorrect_login",
        "email_not_verified",
        "registration_denied",
        "registration_application_pending",
        "registration_application_is_pending",
        "missing_totp_token",
        "incorrect_totp_token",
    ]


class IdentityModelMixin:
    name: str
    published: datetime = Field(..., alias="created")
    inbox_url: types.ActivityPubInbox = Field(..., alias="inbox_uri")
    actor_id: types.ActorId = Field(..., alias="actor_uri")
    instance_id: types.InstanceId


class Site(BaseModel, IdentityModelMixin):
    id: types.SiteId
    sidebar: str | None

    last_refreshed_at: datetime | None = Field(..., alias="fetched")
    icon: types.ImageUrl | None = Field(..., alias="icon_uri")
    banner: types.ImageUrl | None = Field(..., alias="image_uri")
    description: str | None = Field(..., alias="summary")
    public_key: str

    class Config:
        extra = Extra.ignore
        orm_mode = True


class Person(BaseModel, IdentityModelMixin):
    id: types.PersonId
    banned: bool
    local: bool
    bot_account: bool
    deleted: bool = Field(..., alias="is_deleted")

    class Config:
        extra = Extra.ignore
        orm_mode = True


class LocalSite(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    id: types.SiteId
    site_id: types.SiteId
    site_setup: bool
    enable_downvotes: bool
    enable_nsfw: bool
    community_creation_admin_only: bool
    require_email_verification: bool
    application_question: str | None
    private_instance: bool
    default_theme: str
    default_post_listing_type: types.LISTING_TYPES
    legal_information: str | None
    hide_modlog_mod_names: bool
    application_email_admins: bool
    slur_filter_regex: str | None
    actor_name_max_length: int
    federation_enabled: bool
    captcha_enabled: bool
    captcha_difficulty: str
    published: datetime
    updated: datetime | None
    registration_mode: types.REGISTRATION_MODE_OPTIONS
    reports_email_admins: bool
    federation_signed_fetch: bool


class LocalSiteRateLimit(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    local_site_id: types.LocalSiteId
    message: int
    message_per_second: int
    post: int
    post_per_second: int
    register_: int = Field(..., alias="register")
    register_per_second: int
    image: int
    image_per_second: int
    comment: int
    comment_per_second: int
    search: int
    search_per_second: int
    published: datetime
    updated: datetime | None
    import_user_settings: int
    import_user_settings_per_second: int


class SiteAggregates(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    site_id: types.SiteId
    users: int
    posts: int
    comments: int
    communities: int
    users_active_day: int
    users_active_week: int
    users_active_month: int
    users_active_half_year: int


class SiteView(BaseModel):
    class Config:
        extra = Extra.forbid

    site: Site
    local_site: LocalSite
    local_site_rate_limit: LocalSiteRateLimit
    counts: SiteAggregates


class PersonAggregates(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    person_id: types.PersonId
    post_count: int
    comment_count: int


class PersonView(BaseModel):
    class Config:
        extra = Extra.forbid

    person: Person
    counts: PersonAggregates
    is_admin: bool


class LocalUser(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.LocalUserId
    person_id: types.PersonId
    email: str | None
    show_nsfw: bool
    theme: str
    default_sort_type: types.SORT_TYPE_OPTIONS
    default_listing_type: types.LISTING_TYPES
    interface_language: str
    show_avatars: bool
    send_notifications_to_email: bool
    show_scores: bool
    show_bot_accounts: bool
    show_read_posts: bool
    email_verified: bool
    accepted_application: bool
    open_links_in_new_tab: bool
    blur_nsfw: bool
    auto_expand: bool
    infinite_scroll_enabled: bool
    admin: bool
    post_listing_mode: types.POST_LISTING_MODE_OPTIONS
    totp_2fa_enabled: bool
    enable_keyboard_navigation: bool
    enable_animated_images: bool
    collapse_bot_comments: bool


class LocalUserView(BaseModel):
    class Config:
        extra = Extra.forbid

    local_user: LocalUser
    person: Person
    counts: PersonAggregates


class Community(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CommunityId
    name: str
    title: str
    description: str | None
    removed: bool
    published: datetime
    updated: datetime | None
    deleted: bool
    nsfw: bool
    actor_id: types.ActorId
    local: bool
    icon: str | None
    banner: str | None
    hidden: bool
    posting_restricted_to_mods: bool
    instance_id: types.InstanceId


class CommunityFollowerView(BaseModel):
    class Config:
        extra = Extra.forbid

    community: Community
    follower: Person


class CommunityModeratorView(BaseModel):
    class Config:
        extra = Extra.forbid

    community: Community
    moderator: Person


class CommunityBlockView(BaseModel):
    class Config:
        extra = Extra.forbid

    person: Person
    community: Community


class Instance(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.InstanceId
    domain: str
    published: datetime
    updated: datetime | None
    software: str | None
    version: str | None


class InstanceBlockView(BaseModel):
    class Config:
        extra = Extra.forbid

    person: Person
    instance: Instance
    site: Site | None


class PersonBlockView(BaseModel):
    class Config:
        extra = Extra.forbid

    person: Person
    target: Person


class MyUserInfo(BaseModel):
    class Config:
        extra = Extra.forbid

    local_user_view: LocalUserView
    follows: list[CommunityFollowerView]
    moderates: list[CommunityModeratorView]
    community_blocks: list[CommunityBlockView]
    instance_blocks: list[InstanceBlockView]
    person_blocks: list[PersonBlockView]
    discussion_languages: list[types.LanguageId]


class Language(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.LanguageId
    code: str
    name: str


class Tagline(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    local_site_id: types.LocalSiteId
    content: str
    published: datetime
    updated: datetime | None


class CustomEmoji(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CustomEmojiId
    local_site_id: types.LocalSiteId
    shortcode: str
    image_url: str
    alt_text: str
    category: str
    published: datetime
    updated: datetime | None


class CustomEmojiKeyword(BaseModel):
    class Config:
        extra = Extra.forbid

    custom_emoji_id: types.CustomEmojiId
    keyword: str


class CustomEmojiView(BaseModel):
    class Config:
        extra = Extra.forbid

    custom_emoji: CustomEmoji
    keywords: list[CustomEmojiKeyword]


class GetSiteResponse(BaseModel):
    class Config:
        extra = Extra.ignore

    site_view: SiteView
    admins: list[PersonView]
    version: str | None
    my_user: MyUserInfo | None
    all_languages: list[Language]
    discussion_languages: list[types.LanguageId]
    taglines: list[Tagline]
    custom_emojis: list[CustomEmojiView]


class EditSite(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None
    sidebar: str | None
    description: str | None
    icon: str | None
    banner: str | None
    enable_downvotes: bool | None
    enable_nsfw: bool | None
    community_creation_admin_only: bool | None
    require_email_verification: bool | None
    application_question: str | None
    private_instance: bool | None
    default_theme: str | None
    default_post_listing_type: types.LISTING_TYPES | None
    legal_information: str | None
    application_email_admins: bool | None
    hide_modlog_mod_names: bool | None
    discussion_languages: list[types.LanguageId] | None
    slur_filter_regex: str | None
    actor_name_max_length: int | None
    rate_limit_message: int | None
    rate_limit_message_per_second: int | None
    rate_limit_post: int | None
    rate_limit_post_per_second: int | None
    rate_limit_register: int | None
    rate_limit_register_per_second: int | None
    rate_limit_image: int | None
    rate_limit_image_per_second: int | None
    rate_limit_comment: int | None
    rate_limit_comment_per_second: int | None
    rate_limit_search: int | None
    rate_limit_search_per_second: int | None
    federation_enabled: bool | None
    federation_debug: bool | None
    captcha_enabled: bool | None
    captcha_difficulty: str | None
    allowed_instances: list[str] | None
    blocked_instances: list[str] | None
    taglines: list[str] | None
    registration_mode: types.REGISTRATION_MODE_OPTIONS | None
    reports_email_admins: bool | None


class SiteResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    site_view: SiteView
    taglines: list[Tagline]


class CreateSite(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str
    sidebar: str | None
    description: str | None
    icon: str | None
    banner: str | None
    enable_downvotes: bool | None
    enable_nsfw: bool | None
    community_creation_admin_only: bool | None
    require_email_verification: bool | None
    application_question: str | None
    private_instance: bool | None
    default_theme: str | None
    default_post_listing_type: types.LISTING_TYPES | None
    legal_information: str | None
    application_email_admins: bool | None
    hide_modlog_mod_names: bool | None
    discussion_languages: list[types.LanguageId] | None
    slur_filter_regex: str | None
    actor_name_max_length: int | None
    rate_limit_message: int | None
    rate_limit_message_per_second: int | None
    rate_limit_post: int | None
    rate_limit_post_per_second: int | None
    rate_limit_register: int | None
    rate_limit_register_per_second: int | None
    rate_limit_image: int | None
    rate_limit_image_per_second: int | None
    rate_limit_comment: int | None
    rate_limit_comment_per_second: int | None
    rate_limit_search: int | None
    rate_limit_search_per_second: int | None
    federation_enabled: bool | None
    federation_debug: bool | None
    captcha_enabled: bool | None
    captcha_difficulty: str | None
    allowed_instances: list[str] | None
    blocked_instances: list[str] | None
    taglines: list[str] | None
    registration_mode: types.REGISTRATION_MODE_OPTIONS | None


class GetModlog(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_person_id: types.PersonId | None
    community_id: types.CommunityId | None
    page: int | None
    limit: int | None
    type_: types.MOD_LOG_ACTION_TYPES | None
    other_person_id: types.PersonId | None


class ModRemovePost(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    post_id: types.PostId
    reason: str | None
    removed: bool
    when_: str


class Post(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.PostId
    name: str
    url: str | None
    body: str | None
    creator_id: types.PersonId
    community_id: types.CommunityId
    removed: bool
    locked: bool
    published: datetime
    updated: datetime | None
    deleted: bool
    nsfw: bool
    embed_title: str | None
    embed_description: str | None
    thumbnail_url: str | None
    ap_id: str
    local: bool
    embed_video_url: str | None
    language_id: types.LanguageId
    featured_community: bool
    featured_local: bool


class ModRemovePostView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_remove_post: ModRemovePost
    moderator: Person | None
    post: Post
    community: Community


class ModLockPost(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    post_id: types.PostId
    locked: bool
    when_: str


class ModLockPostView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_lock_post: ModLockPost
    moderator: Person | None
    post: Post
    community: Community


class ModFeaturePost(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    post_id: types.PostId
    featured: bool
    when_: str
    is_featured_community: bool


class ModFeaturePostView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_feature_post: ModFeaturePost
    moderator: Person | None
    post: Post
    community: Community


class ModRemoveComment(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    comment_id: types.CommentId
    reason: str | None
    removed: bool
    when_: str


class Comment(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CommentId
    creator_id: types.PersonId
    post_id: types.PostId
    content: str
    removed: bool
    published: datetime
    updated: datetime | None
    deleted: bool
    ap_id: str
    local: bool
    path: str
    distinguished: bool
    language_id: types.LanguageId


class ModRemoveCommentView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_remove_comment: ModRemoveComment
    moderator: Person | None
    comment: Comment
    commenter: Person
    post: Post
    community: Community


class ModRemoveCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    community_id: types.CommunityId
    reason: str | None
    removed: bool
    when_: str


class ModRemoveCommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_remove_community: ModRemoveCommunity
    moderator: Person | None
    community: Community


class ModBanFromCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    other_person_id: types.PersonId
    community_id: types.CommunityId
    reason: str | None
    banned: bool
    expires: str | None
    when_: str


class ModBanFromCommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_ban_from_community: ModBanFromCommunity
    moderator: Person | None
    community: Community
    banned_person: Person


class ModBan(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    other_person_id: types.PersonId
    reason: str | None
    banned: bool
    expires: str | None
    when_: str


class ModBanView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_ban: ModBan
    moderator: Person | None
    banned_person: Person


class ModAddCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    other_person_id: types.PersonId
    community_id: types.CommunityId
    removed: bool
    when_: str


class ModAddCommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_add_community: ModAddCommunity
    moderator: Person | None
    community: Community
    modded_person: Person


class ModTransferCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    other_person_id: types.PersonId
    community_id: types.CommunityId
    when_: str


class ModTransferCommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_transfer_community: ModTransferCommunity
    moderator: Person | None
    community: Community
    modded_person: Person


class ModAdd(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    mod_person_id: types.PersonId
    other_person_id: types.PersonId
    removed: bool
    when_: str


class ModAddView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_add: ModAdd
    moderator: Person | None
    modded_person: Person


class AdminPurgePerson(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    admin_person_id: types.PersonId
    reason: str | None
    when_: str


class AdminPurgePersonView(BaseModel):
    class Config:
        extra = Extra.forbid

    admin_purge_person: AdminPurgePerson
    admin: Person | None


class AdminPurgeCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    admin_person_id: types.PersonId
    reason: str | None
    when_: str


class AdminPurgeCommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    admin_purge_community: AdminPurgeCommunity
    admin: Person | None


class AdminPurgePost(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    admin_person_id: types.PersonId
    community_id: types.CommunityId
    reason: str | None
    when_: str


class AdminPurgePostView(BaseModel):
    class Config:
        extra = Extra.forbid

    admin_purge_post: AdminPurgePost
    admin: Person | None
    community: Community


class AdminPurgeComment(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    admin_person_id: types.PersonId
    post_id: types.PostId
    reason: str | None
    when_: str


class AdminPurgeCommentView(BaseModel):
    class Config:
        extra = Extra.forbid

    admin_purge_comment: AdminPurgeComment
    admin: Person | None
    post: Post


class ModHideCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    community_id: types.CommunityId
    mod_person_id: types.PersonId
    when_: str
    reason: str | None
    hidden: bool


class ModHideCommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    mod_hide_community: ModHideCommunity
    admin: Person | None
    community: Community


class GetModlogResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    removed_posts: list[ModRemovePostView]
    locked_posts: list[ModLockPostView]
    featured_posts: list[ModFeaturePostView]
    removed_comments: list[ModRemoveCommentView]
    removed_communities: list[ModRemoveCommunityView]
    banned_from_community: list[ModBanFromCommunityView]
    banned: list[ModBanView]
    added_to_community: list[ModAddCommunityView]
    transferred_to_community: list[ModTransferCommunityView]
    added: list[ModAddView]
    admin_purged_persons: list[AdminPurgePersonView]
    admin_purged_communities: list[AdminPurgeCommunityView]
    admin_purged_posts: list[AdminPurgePostView]
    admin_purged_comments: list[AdminPurgeCommentView]
    hidden_communities: list[ModHideCommunityView]


class Search(BaseModel):
    class Config:
        extra = Extra.forbid

    q: str
    community_id: types.CommunityId | None
    community_name: str | None
    creator_id: types.PersonId | None
    type_: types.SEARCH_TYPES | None
    sort: types.SORT_TYPE_OPTIONS | None
    listing_type: types.LISTING_TYPES | None
    page: int | None
    limit: int | None


class CommentAggregates(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    score: int
    upvotes: int
    downvotes: int
    published: datetime
    child_count: int


class CommentView(BaseModel):
    class Config:
        extra = Extra.forbid

    comment: Comment
    creator: Person
    post: Post
    community: Community
    counts: CommentAggregates
    creator_banned_from_community: bool
    creator_is_moderator: bool
    creator_is_admin: bool
    subscribed: types.SUBSCRIPTION_TYPES
    saved: bool
    creator_blocked: bool
    my_vote: int | None


class PostAggregates(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    comments: int
    score: int
    upvotes: int
    downvotes: int
    published: datetime
    newest_comment_time: str


class PostView(BaseModel):
    class Config:
        extra = Extra.forbid

    post: Post
    creator: Person
    community: Community
    creator_banned_from_community: bool
    creator_is_moderator: bool
    creator_is_admin: bool
    counts: PostAggregates
    subscribed: types.SUBSCRIPTION_TYPES
    saved: bool
    read: bool
    creator_blocked: bool
    my_vote: int | None
    unread_comments: int


class CommunityAggregates(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    subscribers: int
    posts: int
    comments: int
    published: datetime
    users_active_day: int
    users_active_week: int
    users_active_month: int
    users_active_half_year: int
    subscribers_local: int


class CommunityView(BaseModel):
    class Config:
        extra = Extra.forbid

    community: Community
    subscribed: types.SUBSCRIPTION_TYPES
    blocked: bool
    counts: CommunityAggregates


class SearchResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    type_: types.SEARCH_TYPES
    comments: list[CommentView]
    posts: list[PostView]
    communities: list[CommunityView]
    users: list[PersonView]


class ResolveObject(BaseModel):
    class Config:
        extra = Extra.forbid

    q: str


class ResolveObjectResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comment: CommentView | None
    post: PostView | None
    community: CommunityView | None
    person: PersonView | None


class GetCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CommunityId | None
    name: str | None


class GetCommunityResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    community_view: CommunityView
    site: Site | None
    moderators: list[CommunityModeratorView]
    discussion_languages: list[types.LanguageId]


class EditCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    title: str | None
    description: str | None
    icon: str | None
    banner: str | None
    nsfw: bool | None
    posting_restricted_to_mods: bool | None
    discussion_languages: list[types.LanguageId] | None
    local_only: bool | None


class CommunityResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    community_view: CommunityView
    discussion_languages: list[types.LanguageId]


class CreateCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str
    title: str
    description: str | None
    icon: str | None
    banner: str | None
    nsfw: bool | None
    posting_restricted_to_mods: bool | None
    discussion_languages: list[types.LanguageId] | None
    local_only: bool | None


class HideCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    hidden: bool
    reason: str | None


class ListCommunities(BaseModel):
    class Config:
        extra = Extra.forbid

    type_: types.LISTING_TYPES | None
    sort: types.SORT_TYPE_OPTIONS | None
    show_nsfw: bool | None
    page: int | None
    limit: int | None


class ListCommunitiesResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    communities: list[CommunityView]


class FollowCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    follow: bool


class BlockCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    block: bool


class BlockCommunityResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    community_view: CommunityView
    blocked: bool


class DeleteCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    deleted: bool


class RemoveCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    removed: bool
    reason: str | None


class TransferCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    person_id: types.PersonId


class BanFromCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    person_id: types.PersonId
    ban: bool
    remove_data: bool | None
    reason: str | None
    expires: int | None


class BanFromCommunityResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    person_view: PersonView
    banned: bool


class AddModToCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    person_id: types.PersonId
    added: bool


class AddModToCommunityResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    moderators: list[CommunityModeratorView]


class ReadableFederationState(BaseModel):
    class Config:
        extra = Extra.forbid

    instance_id: types.InstanceId
    last_successful_id: types.ActivityId | None
    last_successful_published_time: str | None
    fail_count: int
    last_retry: str | None
    next_retry: str | None


class InstanceWithFederationState(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.InstanceId
    domain: str
    published: datetime
    updated: datetime | None
    software: str | None
    version: str | None
    federation_state: ReadableFederationState | None


class FederatedInstances(BaseModel):
    class Config:
        extra = Extra.forbid

    linked: list[InstanceWithFederationState]
    allowed: list[InstanceWithFederationState]
    blocked: list[InstanceWithFederationState]


class GetFederatedInstancesResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    federated_instances: FederatedInstances | None


class GetPost(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.PostId | None
    comment_id: types.CommentId | None


class GetPostResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    post_view: PostView
    community_view: CommunityView
    moderators: list[CommunityModeratorView]
    cross_posts: list[PostView]


class EditPost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    name: str | None
    url: str | None
    body: str | None
    nsfw: bool | None
    language_id: types.LanguageId | None


class PostResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    post_view: PostView


class CreatePost(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str
    community_id: types.CommunityId
    url: str | None
    body: str | None
    honeypot: str | None
    nsfw: bool | None
    language_id: types.LanguageId | None


class GetPosts(BaseModel):
    class Config:
        extra = Extra.forbid

    type_: types.LISTING_TYPES | None
    sort: types.SORT_TYPE_OPTIONS | None
    page: int | None
    limit: int | None
    community_id: types.CommunityId | None
    community_name: str | None
    saved_only: bool | None
    liked_only: bool | None
    disliked_only: bool | None
    page_cursor: types.PaginationCursor | None


class GetPostsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    posts: list[PostView]
    next_page: types.PaginationCursor | None


class DeletePost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    deleted: bool


class RemovePost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    removed: bool
    reason: str | None


class MarkPostAsRead(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId | None
    post_ids: list[types.PostId] | None
    read: bool


class SuccessResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    success: bool


class LockPost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    locked: bool


class FeaturePost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    featured: bool
    feature_type: types.POST_FEATURE_TYPES


class CreatePostLike(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    score: int


class SavePost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    save: bool


class CreatePostReport(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    reason: str


class PostReport(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.PostReportId
    creator_id: types.PersonId
    post_id: types.PostId
    original_post_name: str
    original_post_url: str | None
    original_post_body: str | None
    reason: str
    resolved: bool
    resolver_id: types.PersonId | None
    published: datetime
    updated: datetime | None


class PostReportView(BaseModel):
    class Config:
        extra = Extra.forbid

    post_report: PostReport
    post: Post
    community: Community
    creator: Person
    post_creator: Person
    creator_banned_from_community: bool
    my_vote: int | None
    counts: PostAggregates
    resolver: Person | None


class PostReportResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    post_report_view: PostReportView


class ResolvePostReport(BaseModel):
    class Config:
        extra = Extra.forbid

    report_id: types.PostReportId
    resolved: bool


class ListPostReports(BaseModel):
    class Config:
        extra = Extra.forbid

    page: int | None
    limit: int | None
    unresolved_only: bool | None
    community_id: types.CommunityId | None


class ListPostReportsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    post_reports: list[PostReportView]


class GetSiteMetadata(BaseModel):
    class Config:
        extra = Extra.forbid

    url: str


class SiteMetadata(BaseModel):
    class Config:
        extra = Extra.forbid

    title: str | None
    description: str | None
    image: str | None
    embed_video_url: str | None


class GetSiteMetadataResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    metadata: SiteMetadata


class GetComment(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CommentId


class CommentResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_view: CommentView
    recipient_ids: list[types.LocalUserId]


class EditComment(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    content: str | None
    language_id: types.LanguageId | None


class CreateComment(BaseModel):
    class Config:
        extra = Extra.forbid

    content: str
    post_id: types.PostId
    parent_id: types.CommentId | None
    language_id: types.LanguageId | None


class GetComments(BaseModel):
    class Config:
        extra = Extra.forbid

    type_: types.LISTING_TYPES | None
    sort: types.COMMENT_SORT_TYPES | None
    max_depth: int | None
    page: int | None
    limit: int | None
    community_id: types.CommunityId | None
    community_name: str | None
    post_id: types.PostId | None
    parent_id: types.CommentId | None
    saved_only: bool | None
    liked_only: bool | None
    disliked_only: bool | None


class GetCommentsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comments: list[CommentView]


class DeleteComment(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    deleted: bool


class RemoveComment(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    removed: bool
    reason: str | None


class MarkCommentReplyAsRead(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_reply_id: types.CommentReplyId
    read: bool


class CommentReply(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CommentReplyId
    recipient_id: types.PersonId
    comment_id: types.CommentId
    read: bool
    published: datetime


class CommentReplyView(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_reply: CommentReply
    comment: Comment
    creator: Person
    post: Post
    community: Community
    recipient: Person
    counts: CommentAggregates
    creator_banned_from_community: bool
    creator_is_moderator: bool
    creator_is_admin: bool
    subscribed: types.SUBSCRIPTION_TYPES
    saved: bool
    creator_blocked: bool
    my_vote: int | None


class CommentReplyResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_reply_view: CommentReplyView


class DistinguishComment(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    distinguished: bool


class CreateCommentLike(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    score: int


class SaveComment(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    save: bool


class CreateCommentReport(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    reason: str


class CommentReport(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CommentReportId
    creator_id: types.PersonId
    comment_id: types.CommentId
    original_comment_text: str
    reason: str
    resolved: bool
    resolver_id: types.PersonId | None
    published: datetime
    updated: datetime | None


class CommentReportView(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_report: CommentReport
    comment: Comment
    post: Post
    community: Community
    creator: Person
    comment_creator: Person
    counts: CommentAggregates
    creator_banned_from_community: bool
    my_vote: int | None
    resolver: Person | None


class CommentReportResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_report_view: CommentReportView


class ResolveCommentReport(BaseModel):
    class Config:
        extra = Extra.forbid

    report_id: types.CommentReportId
    resolved: bool


class ListCommentReports(BaseModel):
    class Config:
        extra = Extra.forbid

    page: int | None
    limit: int | None
    unresolved_only: bool | None
    community_id: types.CommunityId | None


class ListCommentReportsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_reports: list[CommentReportView]


class EditPrivateMessage(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_id: types.PrivateMessageId
    content: str


class PrivateMessage(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.PrivateMessageId
    creator_id: types.PersonId
    recipient_id: types.PersonId
    content: str
    deleted: bool
    read: bool
    published: datetime
    updated: datetime | None
    ap_id: str
    local: bool


class PrivateMessageView(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message: PrivateMessage
    creator: Person
    recipient: Person


class PrivateMessageResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_view: PrivateMessageView


class CreatePrivateMessage(BaseModel):
    class Config:
        extra = Extra.forbid

    content: str
    recipient_id: types.PersonId


class GetPrivateMessages(BaseModel):
    class Config:
        extra = Extra.forbid

    unread_only: bool | None
    page: int | None
    limit: int | None
    creator_id: types.PersonId | None


class PrivateMessagesResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    private_messages: list[PrivateMessageView]


class DeletePrivateMessage(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_id: types.PrivateMessageId
    deleted: bool


class MarkPrivateMessageAsRead(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_id: types.PrivateMessageId
    read: bool


class CreatePrivateMessageReport(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_id: types.PrivateMessageId
    reason: str


class PrivateMessageReport(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.PrivateMessageReportId
    creator_id: types.PersonId
    private_message_id: types.PrivateMessageId
    original_pm_text: str
    reason: str
    resolved: bool
    resolver_id: types.PersonId | None
    published: datetime
    updated: datetime | None


class PrivateMessageReportView(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_report: PrivateMessageReport
    private_message: PrivateMessage
    private_message_creator: Person
    creator: Person
    resolver: Person | None


class PrivateMessageReportResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_report_view: PrivateMessageReportView


class ResolvePrivateMessageReport(BaseModel):
    class Config:
        extra = Extra.forbid

    report_id: types.PrivateMessageReportId
    resolved: bool


class ListPrivateMessageReports(BaseModel):
    class Config:
        extra = Extra.forbid

    page: int | None
    limit: int | None
    unresolved_only: bool | None


class ListPrivateMessageReportsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    private_message_reports: list[PrivateMessageReportView]


class GetPersonDetails(BaseModel):
    class Config:
        extra = Extra.forbid

    person_id: types.PersonId | None
    username: str | None
    sort: types.SORT_TYPE_OPTIONS | None
    page: int | None
    limit: int | None
    community_id: types.CommunityId | None
    saved_only: bool | None


class GetPersonDetailsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    person_view: PersonView
    comments: list[CommentView]
    posts: list[PostView]
    moderates: list[CommunityModeratorView]


class Register(BaseModel):
    class Config:
        extra = Extra.forbid

    username: str
    password: str
    password_verify: str
    show_nsfw: bool
    email: str | None
    captcha_uuid: str | None
    captcha_answer: str | None
    honeypot: str | None
    answer: str | None


class LoginResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    jwt: str | None
    registration_created: bool
    verify_email_sent: bool


class CaptchaResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    png: str
    wav: str
    uuid: str


class GetCaptchaResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    ok: CaptchaResponse | None


class GetPersonMentions(BaseModel):
    class Config:
        extra = Extra.forbid

    sort: types.COMMENT_SORT_TYPES | None
    page: int | None
    limit: int | None
    unread_only: bool | None


class PersonMention(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.PersonMentionId
    recipient_id: types.PersonId
    comment_id: types.CommentId
    read: bool
    published: datetime


class PersonMentionView(BaseModel):
    class Config:
        extra = Extra.forbid

    person_mention: PersonMention
    comment: Comment
    creator: Person
    post: Post
    community: Community
    recipient: Person
    counts: CommentAggregates
    creator_banned_from_community: bool
    creator_is_moderator: bool
    creator_is_admin: bool
    subscribed: types.SUBSCRIPTION_TYPES
    saved: bool
    creator_blocked: bool
    my_vote: int | None


class GetPersonMentionsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    mentions: list[PersonMentionView]


class MarkPersonMentionAsRead(BaseModel):
    class Config:
        extra = Extra.forbid

    person_mention_id: types.PersonMentionId
    read: bool


class PersonMentionResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    person_mention_view: PersonMentionView


class GetReplies(BaseModel):
    class Config:
        extra = Extra.forbid

    sort: types.COMMENT_SORT_TYPES | None
    page: int | None
    limit: int | None
    unread_only: bool | None


class GetRepliesResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    replies: list[CommentReplyView]


class BanPerson(BaseModel):
    class Config:
        extra = Extra.forbid

    person_id: types.PersonId
    ban: bool
    remove_data: bool | None
    reason: str | None
    expires: int | None


class BanPersonResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    person_view: PersonView
    banned: bool


class BannedPersonsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    banned: list[PersonView]


class BlockPerson(BaseModel):
    class Config:
        extra = Extra.forbid

    person_id: types.PersonId
    block: bool


class BlockPersonResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    person_view: PersonView
    blocked: bool


class Login(BaseModel):
    class Config:
        extra = Extra.forbid

    username_or_email: str
    password: str
    totp_2fa_token: str | None


class DeleteAccount(BaseModel):
    class Config:
        extra = Extra.forbid

    password: str
    delete_content: bool


class PasswordReset(BaseModel):
    class Config:
        extra = Extra.forbid

    email: str


class PasswordChangeAfterReset(BaseModel):
    class Config:
        extra = Extra.forbid

    token: str
    password: str
    password_verify: str


class SaveUserSettings(BaseModel):
    class Config:
        extra = Extra.forbid

    show_nsfw: bool | None
    blur_nsfw: bool | None
    auto_expand: bool | None
    show_scores: bool | None
    theme: str | None
    default_sort_type: types.SORT_TYPE_OPTIONS | None
    default_listing_type: types.LISTING_TYPES | None
    interface_language: str | None
    avatar: str | None
    banner: str | None
    display_name: str | None
    email: str | None
    bio: str | None
    matrix_user_id: str | None
    show_avatars: bool | None
    send_notifications_to_email: bool | None
    bot_account: bool | None
    show_bot_accounts: bool | None
    show_read_posts: bool | None
    discussion_languages: list[types.LanguageId] | None
    open_links_in_new_tab: bool | None
    infinite_scroll_enabled: bool | None
    post_listing_mode: types.POST_LISTING_MODE_OPTIONS | None
    enable_keyboard_navigation: bool | None
    enable_animated_images: bool | None
    collapse_bot_comments: bool | None


class ChangePassword(BaseModel):
    class Config:
        extra = Extra.forbid

    new_password: str
    new_password_verify: str
    old_password: str


class GetReportCount(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId | None


class GetReportCountResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId | None
    comment_reports: int
    post_reports: int
    private_message_reports: int | None


class GetUnreadCountResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    replies: int
    mentions: int
    private_messages: int


class VerifyEmail(BaseModel):
    class Config:
        extra = Extra.forbid

    token: str


class AddAdmin(BaseModel):
    class Config:
        extra = Extra.forbid

    person_id: types.PersonId
    added: bool


class AddAdminResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    admins: list[PersonView]


class GetUnreadRegistrationApplicationCountResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    registration_applications: int


class ListRegistrationApplications(BaseModel):
    class Config:
        extra = Extra.forbid

    unread_only: bool | None
    page: int | None
    limit: int | None


class RegistrationApplication(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    local_user_id: types.LocalUserId
    answer: str
    admin_id: types.PersonId | None
    deny_reason: str | None
    published: datetime


class RegistrationApplicationView(BaseModel):
    class Config:
        extra = Extra.forbid

    registration_application: RegistrationApplication
    creator_local_user: LocalUser
    creator: Person
    admin: Person | None


class ListRegistrationApplicationsResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    registration_applications: list[RegistrationApplicationView]


class ApproveRegistrationApplication(BaseModel):
    class Config:
        extra = Extra.forbid

    id: int
    approve: bool
    deny_reason: str | None


class PurgePerson(BaseModel):
    class Config:
        extra = Extra.forbid

    person_id: types.PersonId
    reason: str | None


class PurgeCommunity(BaseModel):
    class Config:
        extra = Extra.forbid

    community_id: types.CommunityId
    reason: str | None


class PurgePost(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    reason: str | None


class PurgeComment(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    reason: str | None


class EditCustomEmoji(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CustomEmojiId
    category: str
    image_url: str
    alt_text: str
    keywords: list[str]


class CustomEmojiResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    custom_emoji: CustomEmojiView


class CreateCustomEmoji(BaseModel):
    class Config:
        extra = Extra.forbid

    category: str
    shortcode: str
    image_url: str
    alt_text: str
    keywords: list[str]


class DeleteCustomEmoji(BaseModel):
    class Config:
        extra = Extra.forbid

    id: types.CustomEmojiId


class BlockInstance(BaseModel):
    class Config:
        extra = Extra.forbid

    instance_id: types.InstanceId
    block: bool


class BlockInstanceResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    blocked: bool


class GenerateTotpSecretResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    totp_secret_url: str


class UpdateTotp(BaseModel):
    class Config:
        extra = Extra.forbid

    totp_token: str
    enabled: bool


class UpdateTotpResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    enabled: bool


class LoginToken(BaseModel):
    class Config:
        extra = Extra.forbid

    user_id: types.LocalUserId
    published: datetime
    ip: str | None
    user_agent: str | None


class ListPostLikes(BaseModel):
    class Config:
        extra = Extra.forbid

    post_id: types.PostId
    page: int | None
    limit: int | None


class VoteView(BaseModel):
    class Config:
        extra = Extra.forbid

    creator: Person
    score: int


class ListPostLikesResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    post_likes: list[VoteView]


class ListCommentLikes(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_id: types.CommentId
    page: int | None
    limit: int | None


class ListCommentLikesResponse(BaseModel):
    class Config:
        extra = Extra.forbid

    comment_likes: list[VoteView]
