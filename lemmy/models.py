from django.db import models

from users.models import Domain, Identity

from . import choices


class Instance(Domain):
    @property
    def published(self):
        return self.created

    @property
    def software(self):
        if self.nodeinfo:
            software = self.nodeinfo.get("software", {})
            return software.get("name", "unknown")
        return None

    @property
    def version(self):
        if self.nodeinfo:
            software = self.nodeinfo.get("software", {})
            return software.get("version", "unknown")
        return None

    class Meta:
        proxy = True


class Person(Identity):
    banned = models.BooleanField()
    matrix_user_id = models.TextField(blank=True, null=True)
    bot_account = models.BooleanField(default=False)
    ban_expires = models.DateTimeField(blank=True, null=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted is not None

    def __str__(self):
        return self.actor_uri


class Site(Identity):
    sidebar = models.TextField(blank=True, null=True)
    admins = models.ManyToManyField(Person)


class AdminPurgeComment(models.Model):
    admin_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    when_field = models.DateTimeField(db_column="when_")


class AdminPurgeCommunity(models.Model):
    admin_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    when_field = models.DateTimeField(db_column="when_")


class AdminPurgePerson(models.Model):
    admin_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    when_field = models.DateTimeField(db_column="when_")


class AdminPurgePost(models.Model):
    admin_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    community = models.ForeignKey("Community", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    when_field = models.DateTimeField(db_column="when_")


class CaptchaAnswer(models.Model):
    uuid = models.UUIDField(primary_key=True)
    answer = models.TextField()
    published = models.DateTimeField()


class Comment(models.Model):
    creator = models.ForeignKey("Person", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.TextField()
    removed = models.BooleanField()
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField()
    ap_id = models.CharField(unique=True, max_length=255)
    local = models.BooleanField()
    path = models.TextField()
    distinguished = models.BooleanField()
    language = models.ForeignKey("Language", on_delete=models.CASCADE)


class CommentAggregates(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, primary_key=True)
    score = models.BigIntegerField()
    upvotes = models.BigIntegerField()
    downvotes = models.BigIntegerField()
    published = models.DateTimeField()
    child_count = models.IntegerField()
    hot_rank = models.FloatField()
    controversy_rank = models.FloatField()


class CommentLike(models.Model):
    person = models.OneToOneField("Person", on_delete=models.CASCADE, primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "comment"),)


class CommentReply(models.Model):
    recipient = models.ForeignKey("Person", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    read = models.BooleanField()
    published = models.DateTimeField()

    class Meta:
        unique_together = (("recipient", "comment"),)


class CommentReport(models.Model):
    creator = models.ForeignKey("Person", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    original_comment_text = models.TextField()
    reason = models.TextField()
    resolved = models.BooleanField()
    resolver = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        related_name="commentreport_resolver_set",
        blank=True,
        null=True,
    )
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("comment", "creator"),)


class CommentSaved(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    person = models.OneToOneField("Person", on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "comment"),)


class Community(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    removed = models.BooleanField()
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField()
    nsfw = models.BooleanField()
    actor_id = models.CharField(unique=True, max_length=255)
    local = models.BooleanField()
    private_key = models.TextField(blank=True, null=True)
    public_key = models.TextField()
    last_refreshed_at = models.DateTimeField()
    icon = models.TextField(blank=True, null=True)
    banner = models.TextField(blank=True, null=True)
    followers_url = models.CharField(unique=True, max_length=255)
    inbox_url = models.CharField(max_length=255)
    shared_inbox_url = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.BooleanField()
    posting_restricted_to_mods = models.BooleanField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    moderators_url = models.CharField(
        unique=True, max_length=255, blank=True, null=True
    )
    featured_url = models.CharField(unique=True, max_length=255, blank=True, null=True)


class CommunityAggregates(models.Model):
    community = models.OneToOneField(
        Community, on_delete=models.CASCADE, primary_key=True
    )
    subscribers = models.BigIntegerField()
    posts = models.BigIntegerField()
    comments = models.BigIntegerField()
    published = models.DateTimeField()
    users_active_day = models.BigIntegerField()
    users_active_week = models.BigIntegerField()
    users_active_month = models.BigIntegerField()
    users_active_half_year = models.BigIntegerField()
    hot_rank = models.FloatField()


class CommunityBlock(models.Model):
    person = models.OneToOneField("Person", on_delete=models.CASCADE, primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "community"),)


class CommunityFollower(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    person = models.OneToOneField("Person", on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()
    pending = models.BooleanField()

    class Meta:
        unique_together = (("person", "community"),)


class CommunityLanguage(models.Model):
    community = models.OneToOneField(
        Community, on_delete=models.CASCADE, primary_key=True
    )
    language = models.ForeignKey("Language", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("community", "language"),)


class CommunityModerator(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    person = models.OneToOneField("Person", on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "community"),)


class CommunityPersonBan(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    person = models.OneToOneField("Person", on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()
    expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("person", "community"),)


class CustomEmoji(models.Model):
    local_site = models.ForeignKey("LocalSite", on_delete=models.CASCADE)
    shortcode = models.CharField(unique=True, max_length=128)
    image_url = models.TextField(unique=True)
    alt_text = models.TextField()
    category = models.TextField()
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)


class CustomEmojiKeyword(models.Model):
    custom_emoji = models.OneToOneField(
        CustomEmoji, on_delete=models.CASCADE, primary_key=True
    )
    keyword = models.CharField(max_length=128)

    class Meta:
        unique_together = (("custom_emoji", "keyword"),)


class EmailVerification(models.Model):
    local_user = models.ForeignKey("LocalUser", on_delete=models.CASCADE)
    email = models.TextField()
    verification_token = models.TextField()
    published = models.DateTimeField()


class FederationAllowlist(models.Model):
    instance = models.OneToOneField(Instance, on_delete=models.CASCADE)
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)


class FederationBlocklist(models.Model):
    instance = models.OneToOneField(
        "Instance", on_delete=models.CASCADE, primary_key=True
    )
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)


class FederationQueueState(models.Model):
    instance = models.OneToOneField(
        "Instance", on_delete=models.CASCADE, primary_key=True
    )
    last_successful_id = models.BigIntegerField(blank=True, null=True)
    fail_count = models.IntegerField()
    last_retry = models.DateTimeField(blank=True, null=True)
    last_successful_published_time = models.DateTimeField(blank=True, null=True)


class ImageUpload(models.Model):
    local_user = models.ForeignKey("LocalUser", on_delete=models.CASCADE)
    pictrs_alias = models.TextField(primary_key=True)
    pictrs_delete_token = models.TextField()
    published = models.DateTimeField()


class InstanceBlock(models.Model):
    person = models.OneToOneField("Person", on_delete=models.CASCADE)
    instance = models.ForeignKey(Domain, on_delete=models.CASCADE)
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "instance"),)


class Language(models.Model):
    code = models.CharField(max_length=3)
    name = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.code})"


class LocalSite(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    site_setup = models.BooleanField(default=False)
    enable_downvotes = models.BooleanField(default=True)
    enable_nsfw = models.BooleanField(default=False)
    community_creation_admin_only = models.BooleanField(default=True)
    require_email_verification = models.BooleanField(default=True)
    application_question = models.TextField(blank=True, null=True)
    private_instance = models.BooleanField(default=False)
    default_theme = models.TextField()
    default_post_listing_type = models.CharField(
        max_length=20,
        choices=choices.ListingType.choices,
        default=choices.ListingType.Subscribed,
    )
    legal_information = models.TextField(blank=True, null=True)
    hide_modlog_mod_names = models.BooleanField(default=False)
    application_email_admins = models.BooleanField(default=False)
    slur_filter_regex = models.TextField(blank=True, null=True)
    actor_name_max_length = models.IntegerField(default=20)
    federation_enabled = models.BooleanField(default=True)
    captcha_enabled = models.BooleanField(default=False)
    captcha_difficulty = models.CharField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registration_mode = models.CharField(
        max_length=20,
        choices=choices.RegistrationMode.choices,
        default=choices.RegistrationMode.RequireApplication,
    )
    reports_email_admins = models.BooleanField(default=False)
    federation_signed_fetch = models.BooleanField(default=False)


class LocalSiteRateLimit(models.Model):
    local_site = models.OneToOneField(LocalSite, on_delete=models.CASCADE)
    message = models.IntegerField(default=999)
    message_per_second = models.IntegerField(default=60)
    post = models.IntegerField(default=999)
    post_per_second = models.IntegerField(default=60)
    register = models.IntegerField(default=999)
    register_per_second = models.IntegerField(default=3600)
    image = models.IntegerField(default=999)
    image_per_second = models.IntegerField(default=3600)
    comment = models.IntegerField(default=999)
    comment_per_second = models.IntegerField(default=3600)
    search = models.IntegerField(default=999)
    search_per_second = models.IntegerField(default=600)
    import_user_settings = models.IntegerField(default=1)
    import_user_settings_per_second = models.IntegerField(default=86400)
    published = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


class LocalUser(models.Model):
    person = models.OneToOneField("Person", on_delete=models.CASCADE)
    password_encrypted = models.TextField()
    email = models.TextField(unique=True, blank=True, null=True)
    show_nsfw = models.BooleanField()
    theme = models.TextField()
    default_sort_type = models.TextField()  # This field type is a guess.
    default_listing_type = models.TextField()  # This field type is a guess.
    interface_language = models.CharField(max_length=20)
    show_avatars = models.BooleanField()
    send_notifications_to_email = models.BooleanField()
    show_scores = models.BooleanField()
    show_bot_accounts = models.BooleanField()
    show_read_posts = models.BooleanField()
    email_verified = models.BooleanField()
    accepted_application = models.BooleanField()
    totp_2fa_secret = models.TextField(blank=True, null=True)
    open_links_in_new_tab = models.BooleanField()
    infinite_scroll_enabled = models.BooleanField()
    blur_nsfw = models.BooleanField()
    auto_expand = models.BooleanField()
    admin = models.BooleanField()
    post_listing_mode = models.TextField()  # This field type is a guess.
    totp_2fa_enabled = models.BooleanField()
    enable_keyboard_navigation = models.BooleanField()
    enable_animated_images = models.BooleanField()
    collapse_bot_comments = models.BooleanField()

    def __str__(self):
        return self.person.name


class LocalUserLanguage(models.Model):
    local_user = models.OneToOneField(
        LocalUser, on_delete=models.CASCADE, primary_key=True
    )
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("local_user", "language"),)


class LoginToken(models.Model):
    token = models.TextField(primary_key=True)
    user = models.ForeignKey(LocalUser, on_delete=models.CASCADE)
    published = models.DateTimeField()
    ip = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)


class ModAdd(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    other_person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="modadd_other_person_set"
    )
    removed = models.BooleanField()
    when_field = models.DateTimeField(db_column="when_")


class ModAddCommunity(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    other_person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="modaddcommunity_other_person_set",
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    removed = models.BooleanField()
    when_field = models.DateTimeField(db_column="when_")


class ModBan(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    other_person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, related_name="modban_other_person_set"
    )
    reason = models.TextField(blank=True, null=True)
    banned = models.BooleanField()
    expires = models.DateTimeField(blank=True, null=True)
    when_field = models.DateTimeField(db_column="when_")


class ModBanFromCommunity(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    other_person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="modbanfromcommunity_other_person_set",
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    banned = models.BooleanField()
    expires = models.DateTimeField(blank=True, null=True)
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.


class ModFeaturePost(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    featured = models.BooleanField()
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.
    is_featured_community = models.BooleanField()


class ModHideCommunity(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.
    reason = models.TextField(blank=True, null=True)
    hidden = models.BooleanField()


class ModLockPost(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    locked = models.BooleanField()
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.


class ModRemoveComment(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    removed = models.BooleanField()
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.


class ModRemoveCommunity(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    removed = models.BooleanField()
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.


class ModRemovePost(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    removed = models.BooleanField()
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.


class ModTransferCommunity(models.Model):
    mod_person = models.ForeignKey("Person", on_delete=models.CASCADE)
    other_person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="modtransfercommunity_other_person_set",
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    when_field = models.DateTimeField(
        db_column="when_"
    )  # Field renamed because it ended with '_'.


class PasswordResetRequest(models.Model):
    token = models.TextField()
    published = models.DateTimeField()
    local_user = models.ForeignKey(LocalUser, on_delete=models.CASCADE)


class PersonAggregates(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    post_count = models.BigIntegerField(default=0)
    post_score = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)
    comment_score = models.BigIntegerField(default=0)


class PersonBan(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()


class PersonBlock(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    target = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="personblock_target_set"
    )
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "target"),)


class PersonFollower(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    follower = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="personfollower_follower_set",
    )
    published = models.DateTimeField()
    pending = models.BooleanField()

    class Meta:
        unique_together = (("follower", "person"),)


class PersonMention(models.Model):
    recipient = models.ForeignKey(Person, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    read = models.BooleanField()
    published = models.DateTimeField()

    class Meta:
        unique_together = (("recipient", "comment"),)


class PersonPostAggregates(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    read_comments = models.BigIntegerField()
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "post"),)


class Post(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=512, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    removed = models.BooleanField()
    locked = models.BooleanField()
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField()
    nsfw = models.BooleanField()
    embed_title = models.TextField(blank=True, null=True)
    embed_description = models.TextField(blank=True, null=True)
    thumbnail_url = models.TextField(blank=True, null=True)
    ap_id = models.CharField(unique=True, max_length=255)
    local = models.BooleanField()
    embed_video_url = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    featured_community = models.BooleanField()
    featured_local = models.BooleanField()


class PostAggregates(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    comments = models.BigIntegerField()
    score = models.BigIntegerField()
    upvotes = models.BigIntegerField()
    downvotes = models.BigIntegerField()
    published = models.DateTimeField()
    newest_comment_time_necro = models.DateTimeField()
    newest_comment_time = models.DateTimeField()
    featured_community = models.BooleanField()
    featured_local = models.BooleanField()
    hot_rank = models.FloatField()
    hot_rank_active = models.FloatField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    controversy_rank = models.FloatField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    scaled_rank = models.FloatField()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    score = models.SmallIntegerField()
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "post"),)


class PostRead(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "post"),)


class PostReport(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    original_post_name = models.CharField(max_length=200)
    original_post_url = models.TextField(blank=True, null=True)
    original_post_body = models.TextField(blank=True, null=True)
    reason = models.TextField()
    resolved = models.BooleanField()
    resolver = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="postreport_resolver_set",
        blank=True,
        null=True,
    )
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("post", "creator"),)


class PostSaved(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    published = models.DateTimeField()

    class Meta:
        unique_together = (("person", "post"),)


class PrivateMessage(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="privatemessage_recipient_set"
    )
    content = models.TextField()
    deleted = models.BooleanField()
    read = models.BooleanField()
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
    ap_id = models.CharField(unique=True, max_length=255)
    local = models.BooleanField()


class PrivateMessageReport(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    private_message = models.ForeignKey(PrivateMessage, on_delete=models.CASCADE)
    original_pm_text = models.TextField()
    reason = models.TextField()
    resolved = models.BooleanField()
    resolver = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="privatemessagereport_resolver_set",
        blank=True,
        null=True,
    )
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("private_message", "creator"),)


class ReceivedActivity(models.Model):
    ap_id = models.TextField(primary_key=True)
    published = models.DateTimeField()


class RegistrationApplication(models.Model):
    local_user = models.OneToOneField(LocalUser, on_delete=models.CASCADE)
    answer = models.TextField()
    admin = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    deny_reason = models.TextField(blank=True, null=True)
    published = models.DateTimeField()


class Secret(models.Model):
    jwt_secret = models.CharField()


class SentActivity(models.Model):
    id = models.BigAutoField(primary_key=True)
    ap_id = models.TextField(unique=True)
    data = models.TextField()  # This field type is a guess.
    sensitive = models.BooleanField()
    published = models.DateTimeField()
    send_inboxes = models.TextField()  # This field type is a guess.
    send_community_followers_of = models.IntegerField(blank=True, null=True)
    send_all_instances = models.BooleanField()
    actor_type = models.TextField()  # This field type is a guess.
    actor_apub_id = models.TextField(blank=True, null=True)


class SiteAggregates(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    users = models.BigIntegerField(default=0)
    posts = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    communities = models.BigIntegerField(default=0)
    users_active_day = models.BigIntegerField(default=0)
    users_active_week = models.BigIntegerField(default=0)
    users_active_month = models.BigIntegerField(default=0)
    users_active_half_year = models.BigIntegerField(default=0)


class SiteLanguage(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, primary_key=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("site", "language"),)


class Tagline(models.Model):
    local_site = models.ForeignKey(LocalSite, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField()
    updated = models.DateTimeField(blank=True, null=True)
