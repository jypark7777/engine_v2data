from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
import traceback

class CrawlRecord(models.Model):
    from_source_type = {
        (0,'Request'),
        (1,'External Post API'),
        (2, 'Lambda'),
        (3, 'lambda Profile'),
        (4, 'Lambda Tag'),
        (5,'Lambda Request'),
    }

    from_source = models.IntegerField(default=0, blank=True, choices=from_source_type)
    crawl_type = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='인스타 크롤링 시간', auto_now_add=True, blank=True)

class BaseModel(models.Model):
    record =  models.ForeignKey(CrawlRecord, on_delete=models.SET_NULL, verbose_name='크롤링 레코드', null=True, blank=True, related_name="%(class)s")
    created_time = models.DateTimeField(verbose_name='생성 시간', default=now, blank=True)
    updated_time = models.DateTimeField(verbose_name='수정 시간', default=now, blank=True)
    snap_time = models.DateTimeField(verbose_name='스냅 생성 시간', default=now, blank=True)
    snap_date = models.DateField(verbose_name='스냅 생성 날짜', default=now, blank=True)

    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()
        try:
            super(BaseModel, self).save()
        except:
            print('save error : ', self.__class__.__name__, traceback.format_exc())
            pass

    def jsonToClass(self, json):
        for key, value in json.items():
            try:
                if hasattr(self, 'insta_pk') and ('pk' == key or 'insta_pk' == key):
                    self.insta_pk = value
                elif hasattr(self, 'created_at') and 'created_at' == key:
                    self.created_at = datetime.fromtimestamp(value)
                elif hasattr(self, 'taken_at') and 'taken_at' == key:
                    utc_timezone = timezone.utc
                    self.taken_at = datetime.fromtimestamp(value, utc_timezone)
                elif hasattr(self, 'hd_profile_pic_url_info') and 'hd_profile_pic_url_info' == key:
                    if 'url' in value:
                        self.hd_profile_pic_url = value['url']
                elif hasattr(self, 'insta_id') and 'id' == key:
                    self.insta_id = value
                elif hasattr(self, key):
                    setattr(self, key, value)
                # else:
                #     print(key,' - ', value)
            except:
                # print('set attr : ', traceback.format_exc())
                pass


    class Meta:
        abstract = True

class CrawlProfileImage(BaseModel):
    url = models.URLField(max_length=500, verbose_name='인스타 프로필 이미지',null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)


class CrawlUserProfileBase(BaseModel):
    is_profile_crawled = models.BooleanField(null=True,verbose_name='인스타 프로필 크롤링 유무', blank=True, default=False)
    is_analy_requirements = models.BooleanField(null=True,verbose_name='인스타 프로필 분석 기본 조건 충족', blank=True, default=False, db_index=True)
    is_analy_complete = models.BooleanField(null=True, verbose_name='유저 분석 유무', blank=True, default=False)
    is_report_complete = models.BooleanField(null=True, verbose_name='리포트 생성 유무', blank=True, default=False)

    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, unique=True)
    username = models.CharField(max_length=50, verbose_name='인스타 유저 네임',null=True, blank=True, db_index=True)
    full_name = models.CharField(max_length=50, verbose_name='인스타 풀 네임',null=True, blank=True)
    biography =  models.TextField(null=True, blank=True) #UTF8_MB

    profile_pic_url = models.URLField(max_length=500, verbose_name='인스타 프로필 이미지',null=True, blank=True)
    hd_profile_pic_url = models.URLField(max_length=500, verbose_name='인스타 HD 프로필 이미지',null=True, blank=True) # HD, 내가만든것

    is_private = models.BooleanField(null=True,verbose_name='인스타 비공개 유무', blank=True, default=False)
    is_verified = models.BooleanField(null=True,verbose_name='인스타 인증 유무', blank=True, default=False)
    public_phone_number = models.CharField(max_length=100, null=True, blank=True)
    public_email = models.EmailField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    is_business = models.BooleanField(null=True, blank=True )
    is_professional = models.BooleanField(null=True, blank=True )

    is_business_account = models.BooleanField(null=True, blank=True )
    is_professional_account = models.BooleanField(null=True, blank=True )

    business_email = models.EmailField(max_length=200, null=True, blank=True)
    business_phone_number = models.CharField(max_length=100, null=True, blank=True)
    business_category_name = models.CharField(max_length=100, null=True, blank=True)
    category_enum = models.CharField(max_length=100, null=True, blank=True)
    category_name = models.CharField(max_length=100, null=True, blank=True)
    highlight_reel_count = models.IntegerField(null=True, blank=True)

    media_count = models.IntegerField(null=True, blank=True)
    following_count = models.IntegerField(null=True, blank=True)
    follower_count = models.IntegerField(null=True, blank=True)


    has_chaining = models.BooleanField(null=True, blank=True, default=False)
    should_show_public_contacts = models.BooleanField(null=True, blank=True, default=False)
    public_phone_country_code = models.CharField(max_length=100, null=True, blank=True)
    instagram_location_id = models.CharField(max_length=100, null=True, blank=True)
    contact_phone_number = models.CharField(max_length=100, null=True, blank=True)
    has_anonymous_profile_picture = models.BooleanField(null=True, blank=True, default=False)
    external_url = models.URLField(max_length=500, null=True, blank=True)

    direct_messaging = models.URLField(max_length=100, null=True, blank=True)
    is_favorite = models.BooleanField(null=True, blank=True, default=False)
    total_igtv_videos = models.IntegerField(null=True, blank=True)
    address_street = models.CharField(max_length=500, null=True, blank=True)
    mutual_followers_count = models.IntegerField(null=True, blank=True)
    business_contact_method = models.CharField(max_length=100, null=True, blank=True)

    geo_media_count = models.IntegerField(null=True, blank=True)

    fb_page_call_to_action_id = models.CharField(max_length=100, null=True, blank=True)

    can_hide_public_contacts = models.BooleanField(null=True, blank=True,default=False)

    city_id = models.BigIntegerField(null=True, blank=True)
    city_name = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    address_street = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    usertags_count = models.IntegerField(null=True, blank=True)
    is_potential_business = models.BooleanField(null=True, blank=True)
    auto_expand_chaining = models.BooleanField(null=True, blank=True)
    can_be_reported_as_fraud = models.BooleanField(null=True, blank=True)
    is_interest_account = models.BooleanField(null=True, blank=True)
    has_highlight_reels = models.BooleanField(null=True, blank=True)

    following_tag_count = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "크롤링된 프로필"
        verbose_name_plural = "크롤링된 프로필"
        # unique_together = ['insta_pk', 'record']


class CrawlUserProfileSnapshot(CrawlUserProfileBase):
    class Meta:
        unique_together = ['insta_pk', 'snap_date']

class CrawlUserProfile(CrawlUserProfileBase):
    is_transfile = models.BooleanField(null=True, blank=True, default=False)


class CrawlPostBase(BaseModel):
    # is_analy_requirements = models.BooleanField(null=True,verbose_name='인스타 포스팅 분석 기본 조건 충족(댓글,좋아요 데이터 있음)', blank=True, default=False)
    user =  models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='크롤링된 프로필', null=True, blank=True, related_name="%(class)s")
    can_viewer_save = models.BooleanField(null=True, blank=True, default=False)
    can_see_insights_as_brand = models.BooleanField(null=True, blank=True, default=False)
    organic_tracking_token = models.CharField(max_length=500, null=True, blank=True)
    can_viewer_reshare = models.BooleanField(null=True, blank=True, default=False)
    max_num_visible_preview_comments = models.IntegerField(null=True, blank=True)
    filter_type = models.IntegerField(verbose_name='유저 아이디' , null=True, blank=True)
    client_cache_key = models.CharField(max_length=100, null=True, blank=True)
    comment_likes_enabled = models.BooleanField(null=True, blank=True, default=False)
    media_type = models.IntegerField(null=True, blank=True)
    carousel_media_count = models.BigIntegerField(null=True, blank=True)
    insta_id = models.CharField(max_length=100,null=True, blank=True)
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)

    lat = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    photo_of_you = models.BooleanField(null=True, blank=True, default=False)
    comment_threading_enabled = models.BooleanField(null=True, blank=True, default=False)

    like_count = models.BigIntegerField(null=True, blank=True, default=0)
    comment_count = models.BigIntegerField(null=True, blank=True, default=0)

    direct_reply_to_author_enabled = models.BooleanField(null=True, blank=True, default=False)
    has_liked = models.BooleanField(null=True, blank=True, default=False)
    caption_is_edited = models.BooleanField(null=True, blank=True, default=False)
    has_more_comments = models.BooleanField(null=True, blank=True, default=False)
    inline_composer_display_condition = models.CharField(max_length=100,null=True, blank=True)
    can_view_more_preview_comments = models.BooleanField(null=True, blank=True, default=False)

    taken_at = models.DateTimeField(verbose_name='포스팅 시간', null=True, blank=True)

    accessibility_caption = models.CharField(max_length=1000, null=True, blank=True)
    is_video = models.BooleanField(null=True, blank=True, default=False)
    video_view_count = models.BigIntegerField(null=True, blank=True)

    typename = models.CharField(max_length=100,null=True, blank=True)

    def get_user_insta_pk(self):
        return self.user.insta_pk

    def get_caption_text(self):
        caption = self.crawlpostcaption.exclude(text=None).last()
        if caption != None:
            return caption.text
        else:
             return None

    def get_caption_text_document(self):
        try:
            return self.crawlpostcaption.last().text
        except:
            return None

    def get_caption(self):
        caption = self.crawlpostcaption.exclude(text=None).last()
        # print('get_caption : ' , caption.text)
        # print('get_caption2 : ' , CrawlPostCaption.objects.filter(post=self).count())
        return caption

    def get_video_image(self):
        image = self.video.order_by('-width', '-created_time').first()
        return image

    def get_image(self):
        image = self.image.order_by('-created_time').first()
        # print(image, self.image.count())
        if image == None:
            image = self.video.order_by('-width', '-created_time').first()
        return image


    # def __str__(self):
    #     # caption = self.get_caption()
    #     # if caption != None:
    #     #     return caption.text
    #     # if self.user != None:
    #     #     return self.user + '의 포스팅'
    #     return self.__str__()

    class Meta:
        abstract = True
        verbose_name = "크롤링 된 포스트"
        verbose_name_plural = "크롤링 된 포스트"


class CrawlPostSnapshot(CrawlPostBase):
    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, db_index=True)
    # class Meta:
    #     unique_together = ['insta_pk', 'snap_date']


class CrawlPost(CrawlPostBase):
    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, unique=True)
    sidecar_parent =  models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, related_name="sidecar_children")
    def get_post_user_id(self):
        try:
            return self.user.insta_pk
        except:
            return None

    IMAGE, VIDEO, CAROUSEL = (0,1,2)

    def get_media_type(self):
        if self.is_video or self.video.all().exists():
            return 1
        if self.media.all().exists() or self.sidecar_children.all().exists():
            return 2
        return 0

    def is_sidecar_child(self):
        if self.sidecar_parent != None:
            return True
        return False


class CrawlPostCaptionBase(BaseModel):
    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, unique=True)
    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트', null=True, blank=True, related_name='%(class)s')
    bit_flags = models.IntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True,db_index=True)
    did_report_as_spam = models.BooleanField(null=True, blank=True)
    media_id = models.BigIntegerField(null=True, blank=True)
    created_at_utc = models.BigIntegerField(null=True, blank=True)
    share_enabled = models.BooleanField(null=True, blank=True, default=False)
    content_type = models.CharField(max_length=20,null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20,null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='포스팅 시간', null=True, blank=True)

    def get_post_user_id(self):
        if self.user_id != None:
            return self.user_id
        return self.post.user.insta_pk

    def created_at_to_string(self):
        return str(self.created_at)

    def depth_to_string(self):
        return 0

    class Meta:
        abstract = True
        verbose_name = "크롤링된 포스트 글내용"
        verbose_name_plural = "크롤링된 포스트 글내용"


# class CrawlPostCaptionSnapshot(CrawlPostCaptionBase):
#     class Meta:
#         unique_together = ['insta_pk', 'snap_date']


class CrawlPostCaption(CrawlPostCaptionBase):
    pass

class CrawlPostLiker(BaseModel):

    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 대상 포스트', null=True, blank=True, related_name="liker")
    user = models.ForeignKey('CrawlUserProfile', on_delete=models.SET_NULL, verbose_name='크롤링된 유저', null=True, blank=True, related_name="liker")

    class Meta:
        unique_together = ['post', 'user']
        verbose_name = "크롤링된 포스트 Liker"
        verbose_name_plural = "크롤링된 포스트 Liker"


class CrawlUserSimilar(BaseModel):

    target_user = models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='대상자', null=True, blank=True, related_name='similars')
    user = models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='비슷한 계정들', null=True, blank=True, related_name='similar')

    class Meta:
        unique_together = ['target_user', 'user']
        verbose_name = "크롤링된 비슷한 계정들"
        verbose_name_plural = "크롤링된 비슷한 계정들"

class CrawlUserFollower(BaseModel):

    target_user = models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='대상자 (팔로잉 받은사람)', null=True, blank=True, related_name='follower')
    user = models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='팔로워 (팔로잉 한사람)', null=True, blank=True, related_name='following')

    class Meta:
        unique_together = ['target_user', 'user']
        verbose_name = "크롤링된 프로필 팔로워"
        verbose_name_plural = "크롤링된 프로필 팔로워"

#carousel_media - [image_versions2 - candidates[0], video_versions-[0] ]
#image_versions2 - candidates[0]



class CrawlPostLikerProxy(CrawlPostLiker):
    class Meta:
        proxy = True
        verbose_name = "수집 반응 오디언스 프로필"
        verbose_name_plural = "수집 반응 오디언스 프로필"

class CrawlUserProfileProxy(CrawlUserProfile):
    class Meta:
        proxy = True
        verbose_name = "수집 인플루언서 프로필"
        verbose_name_plural = "수집 인플루언서 프로필"


class CrawlUserFollowerProxy(CrawlUserFollower):
    class Meta:
        proxy=True
        verbose_name = "수집 구독 오디언스 프로필"
        verbose_name_plural = "수집 구독 오디언스 프로필"




class CrawlCarouselMedia(BaseModel):
    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, unique=True)
    insta_id = models.CharField(max_length=100, null=True, blank=True, unique=True)

    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트', null=True, blank=True, related_name='media')
    carousel_parent_id = models.CharField(max_length=50, null=True, blank=True)
    media_type = models.IntegerField(null=True, blank=True)
    original_width = models.IntegerField(null=True, blank=True)
    original_height = models.IntegerField(null=True, blank=True)

    video_codec = models.CharField(max_length=50, null=True, blank=True)
    is_dash_eligible = models.IntegerField(null=True, blank=True)
    video_duration = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    number_of_qualities =  models.IntegerField(null=True, blank=True)

class CrawlPostImageVersion2Candidate(BaseModel):
    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트', null=True, blank=True, related_name='image')
    carousel_media =  models.ForeignKey(CrawlCarouselMedia, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트 미디어', null=True, blank=True, related_name='image')

    url = models.URLField(max_length=500, verbose_name='인스타 이미지',null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)


class CrawlPostVideoVersion(BaseModel):
    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트', null=True, blank=True, related_name='video')
    carousel_media =  models.ForeignKey(CrawlCarouselMedia, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트 미디어', null=True, blank=True, related_name='video')

    insta_id = models.BigIntegerField(null=True, blank=True)

    url = models.URLField(max_length=500, verbose_name='인스타 영상',null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)

class CrawlPostComment(BaseModel):

    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, unique=True)
    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트', null=True, blank=True, related_name="%(class)s")
    user = models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='크롤링된 유저', null=True, blank=True, related_name="%(class)s", db_index=True)
    has_liked_comment = models.BooleanField(null=True,verbose_name='댓글 좋아요', blank=True, default=False)
    text = models.TextField(verbose_name='댓글 내용',null=True, blank=True) #UTF8_MB
    inline_composer_display_condition = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    content_type = models.CharField(max_length=50, null=True, blank=True)
    created_at_utc = models.BigIntegerField(null=True, blank=True)
    share_enabled = models.BooleanField(null=True, blank=True, default=False)
    comment_like_count = models.BigIntegerField( null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    bit_flags = models.IntegerField(null=True, blank=True)
    did_report_as_spam = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(verbose_name='댓글 시간', null=True, blank=True)

    def get_post_user_id(self):
        try:
            return self.post.user.insta_pk
        except:
            return None

    class Meta:
        verbose_name = "크롤링된 포스트 댓글"
        verbose_name_plural = "크롤링된 포스트 댓글"


class CrawlPostLocation(BaseModel):
    insta_pk = models.BigIntegerField(verbose_name='인스타 PK' , null=True, blank=True, unique=True)
    post = models.ManyToManyField(CrawlPost, verbose_name='연관 포스팅', blank=True, related_name="%(class)s")
    external_source = models.CharField(max_length=100, null=True, blank=True)
    facebook_places_id = models.BigIntegerField(null=True, blank=True)
    lat = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

class CrawlPostUserTags(BaseModel):
    post =  models.ForeignKey(CrawlPost, on_delete=models.SET_NULL, verbose_name='크롤링된 포스트', null=True, blank=True, related_name="%(class)s")
    user = models.ForeignKey(CrawlUserProfile, on_delete=models.SET_NULL, verbose_name='태그된 유저', null=True, blank=True, related_name="%(class)s")
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)



class CrawlSearchTagBase(BaseModel):
    '''
        insta_id Snap은 유니크 끄기
    '''
    insta_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    media_count = models.BigIntegerField(verbose_name='미디어 갯수' , null=True, blank=True)

    profile_pic_url = models.URLField(max_length=500, verbose_name='인스타 프로필 이미지',null=True, blank=True)
    formatted_media_count = models.CharField(max_length=100, null=True, blank=True)
    use_default_avatar = models.BooleanField(null=True, blank=True, default=False)

    allow_following = models.BooleanField(null=True, blank=True, default=False)
    is_following = models.BooleanField(null=True, blank=True, default=False)
    is_top_media_only = models.BooleanField(null=True, blank=True, default=False)


    search_result_subtitle = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        abstract = True
        verbose_name = "해시태그 검색 결과"
        verbose_name_plural = "해시태그 검색 결과"


class CrawlSearchTagRelatedPost(models.Model):
    searchtag = models.ForeignKey('CrawlSearchTag', on_delete=models.CASCADE, related_name='related_posts')
    post = models.ForeignKey(CrawlPost, on_delete=models.CASCADE, related_name='related_tags')

    is_top = models.BooleanField(null=True,verbose_name='인스타 포스팅 탑 유무', blank=False, default=False)

    record =  models.ForeignKey(CrawlRecord, on_delete=models.SET_NULL, verbose_name='크롤링 레코드', null=True, blank=True, related_name="%(class)s")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class CrawlRelatedTag(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class CrawlSearchTag(CrawlSearchTagBase):
    is_tag_crawled = models.BooleanField(null=True,verbose_name='인스타 크롤링 유무', blank=True, default=False)
    is_analy_requirements = models.BooleanField(null=True,verbose_name='인스타 분석 기본 조건 충족', blank=True, default=False)
    is_analy_complete = models.BooleanField(null=True, verbose_name='분석 유무', blank=True, default=False)
    is_report_complete = models.BooleanField(null=True, verbose_name='리포트 생성 유무', blank=True, default=False)

    from_search_tag = models.ManyToManyField("self", verbose_name="검색한 키워드 해시태그", blank=True, related_name='search_tags', symmetrical=False)
    related_tag = models.ManyToManyField(CrawlRelatedTag, verbose_name="연관 해시태그", blank=True)

    posts =  models.ManyToManyField(CrawlPost, verbose_name='크롤링된 연관 포스팅', blank=True, related_name="searchtags", through='CrawlSearchTagRelatedPost', through_fields=('searchtag', 'post'))

    def get_image(self):
        if self.profile_pic_url != None:
            return self.profile_pic_url

        image = None

        return image


class CrawlSearchTagSnapshot(CrawlSearchTagBase):
    pass

class CrawlSearchTagProxy(CrawlSearchTag):
    class Meta:
        proxy = True
        verbose_name = "해시태그 검색기"
        verbose_name_plural = "해시태그 검색기"


class CrawlLocationRelatedPost(models.Model):
    location = models.ForeignKey('CrawlLocationFeed', on_delete=models.CASCADE, related_name='related_posts')
    post = models.ForeignKey(CrawlPost, on_delete=models.CASCADE, related_name='related_location')

    is_top = models.BooleanField(null=True,verbose_name='인스타 포스팅 탑 유무', blank=False, default=False)

    record =  models.ForeignKey(CrawlRecord, on_delete=models.SET_NULL, verbose_name='크롤링 레코드', null=True, blank=True, related_name="%(class)s")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class CrawlLocationFeedBase(BaseModel):
    '''
        insta_id Snap은 유니크 끄기
    '''
    insta_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    media_count = models.BigIntegerField(verbose_name='미디어 갯수' , null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        abstract = True
        verbose_name = "위치 피드 검색 결과"
        verbose_name_plural = "위치 피드 검색 결과"


class CrawlLocationFeed(CrawlLocationFeedBase):
    location = models.OneToOneField(CrawlPostLocation, on_delete=models.CASCADE)
    is_tag_crawled = models.BooleanField(null=True,verbose_name='인스타 크롤링 유무', blank=True, default=False)
    is_analy_requirements = models.BooleanField(null=True,verbose_name='인스타 분석 기본 조건 충족', blank=True, default=False)
    is_analy_complete = models.BooleanField(null=True, verbose_name='분석 유무', blank=True, default=False)
    is_report_complete = models.BooleanField(null=True, verbose_name='리포트 생성 유무', blank=True, default=False)

    profile_pic_url = models.URLField(max_length=500, verbose_name='인스타 프로필 이미지',null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    blurb = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    searchtags = models.ManyToManyField(CrawlSearchTag, verbose_name="연관 해시태그", blank=True)

    posts =  models.ManyToManyField(CrawlPost, verbose_name='크롤링된 연관 포스팅', blank=True, related_name="locationfeed", through='CrawlLocationRelatedPost', through_fields=('location', 'post'))

    def get_image(self):
        if self.profile_pic_url != None:
            return self.profile_pic_url

        image = None

        return image


class CrawlLocationFeedSnapshot(CrawlLocationFeedBase):
    pass
