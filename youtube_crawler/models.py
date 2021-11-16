from django.db import models
from django.utils.timezone import now
from django.utils import timezone
import traceback


class CrawlRecord(models.Model):
    from_source_type = {
        (0,'Request'),
        (1,'Youtube Poza API'),
    }

    from_source = models.IntegerField(default=0, blank=True, choices=from_source_type)
    crawl_type = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='유튜브 크롤링 시간', auto_now_add=True, blank=True)


class BaseModel(models.Model):
    record =  models.ManyToManyField(CrawlRecord, verbose_name='크롤링 레코드', related_name="%(class)s")
    created_time = models.DateTimeField(verbose_name='생성 시간', default=now, blank=True)
    updated_time = models.DateTimeField(verbose_name='수정 시간', default=now, blank=True)
    snap_time = models.DateTimeField(verbose_name='스냅 생성 시간', default=now, blank=True)
    snap_date = models.DateField(verbose_name='스냅 생성 날짜', default=now, blank=True)


    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()
        try:
            super(BaseModel, self).save(*args, **kwargs)
        except:
            pass
            # print('save error : ', self.__class__.__name__, traceback.format_exc())

    JSON_PASS_FIELD = ['ForeignKey', 'ManyToManyField', 'OneToOneField']
    def jsonToClass(self, json):
        for key, value in json.items():
            try:
                # if hasattr(self, 'publishedAt') and 'publishedAt' == key:
                #     self.publishedAt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                # elif hasattr(self, key):
                if hasattr(self, key):
                    if self._meta.get_field(key).get_internal_type() not in self.JSON_PASS_FIELD:
                        setattr(self, key, value)
            except:
                print('jsonToClass : ', traceback.format_exc())
                # pass
    class Meta:
        abstract = True

class YoutubeBaseModel(BaseModel):
    etag = models.CharField(max_length=255, null=True, blank=True)
    kind = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

class YoutubeSearchResult(YoutubeBaseModel):
    video = models.ForeignKey('YoutubeVideo',verbose_name='비디오', null=True, blank=True, on_delete=models.SET_NULL)
    channel = models.ForeignKey('YoutubeChannel',verbose_name='채널', null=True, blank=True, on_delete=models.SET_NULL,related_name='searchresult' )

class YoutubeSearchResultId(YoutubeBaseModel):
    result = models.ForeignKey('YoutubeSearchResult',verbose_name='결과', null=True, blank=True, on_delete=models.CASCADE)

    videoId = models.CharField(max_length=255, null=True, blank=True)
    channelId = models.CharField(max_length=255, null=True, blank=True)
    playlistId = models.CharField(max_length=255, null=True, blank=True)

class YoutubeSearchResultSnippet(YoutubeBaseModel):
    result = models.ForeignKey('YoutubeSearchResult',verbose_name='결과', null=True, blank=True, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=True, blank=True)
    publishedAt = models.DateTimeField(verbose_name='publishedAt', null=True, blank=True)
    channelId = models.CharField(max_length=255, null=True, blank=True)
    channelTitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class SearchKeywordBase(YoutubeBaseModel):
    keyword = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    totalResults = models.BigIntegerField(verbose_name='비디오 갯수' , null=True, blank=True)

    results =  models.ManyToManyField(YoutubeSearchResult, verbose_name='연관 결과', blank=True)

    def __str__(self):
        return '%s' % self.keyword

    class Meta:
        abstract = True
        verbose_name = "키워드 종합검색 결과"
        verbose_name_plural = "키워드 종합검색 결과"

class SearchKeyword(SearchKeywordBase):
    pass

class SearchKeywordSnap(SearchKeywordBase):
    pass


"""

유튜브 채널 

"""
class YoutubeChannelManager(models.Manager):

    def get_queryset(self):
        qs = super(YoutubeChannelManager, self).get_queryset()
        return qs.select_related('snippet', 'statistics', 'contentDetails', 'status')

class YoutubeChannel(YoutubeBaseModel):
    channel_id = models.CharField(max_length=70, verbose_name='채널 아이디', unique=True, default=0)

    topicDetails = models.ManyToManyField('YoutubeTopicDetail', blank=True, related_name="channels")

    snippet = models.OneToOneField('YoutubeChannelSnippet',verbose_name='snippet', null=True, blank=True, on_delete=models.SET_NULL)
    statistics = models.OneToOneField('YoutubeChannelStatistics',verbose_name='statistics', null=True, blank=True, on_delete=models.SET_NULL)
    contentDetails = models.OneToOneField('YoutubeChannelContentDetails',verbose_name='contentDetails', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.OneToOneField('YoutubeChannelStatus',verbose_name='status', null=True, blank=True, on_delete=models.SET_NULL)

    def get_title(self):
        try:
            return '%s' % self.snippet.title
        except:
            return None
        # return ''

    def get_description(self):
        try:
            return '%s' % self.snippet.description
        except:
            return None

    def get_subscriberCount(self):
        try:
            return self.snippet.subscriberCount
        except:
            return None

    def __str__(self):
        return '%s (%s)' % (self.get_title(), self.channel_id)

    objects = YoutubeChannelManager()


class YoutubeChannelSnippetBase(YoutubeBaseModel):
    type_regions = {
        (0, '한국'),
        (1, '미국' ),
        (2, '영국' ),
    }
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s")
    title = models.CharField(max_length=255, verbose_name='채널명', null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name='채널설명', null=True, blank=True)
    publishedAt = models.DateTimeField(verbose_name='publishedAt', null=True, blank=True)

    def get_channel_id(self):
        return self.channel.channel_id
        # return ''

    # '''
    #     아래는 새로 정의한 데이터
    # '''
    # logo = models.ImageField(max_length=455, verbose_name='채널 로고', null=True, blank=True)
    # main_image = models.ImageField(max_length=455, verbose_name='채널 메인 이미지', null=True, blank=True)
    # profile_image = models.ImageField(max_length=455, verbose_name='채널 프로필 이미지', null=True, blank=True)
    #
    # category = models.IntegerField(verbose_name='채널 카테고리' , null=True, blank=True)
    #
    # subscriber = models.BigIntegerField(verbose_name='채널 구독자 수' , null=True, blank=True)
    # video_count = models.BigIntegerField(verbose_name='채널 비디오 수' , null=True, blank=True)
    # view_count = models.BigIntegerField(verbose_name='채널 비디오 전체 조회 수' , null=True, blank=True)
    # join_at = models.DateField(verbose_name='채널 가입일', null=True, blank=True)
    #
    # regions = models.IntegerField(verbose_name='지역 구분' , null=True, blank=True, default=0, choices=type_regions)


    def __str__(self):
        if self.title == None:
            return self.channel_id
        return self.title

    class Meta:
        abstract = True
        verbose_name = "유튜브 채널 정보"
        verbose_name_plural = "유튜브 채널 정보"


class YoutubeChannelSnippet(YoutubeChannelSnippetBase):
    pass

class YoutubeChannelSnippetSnap(YoutubeChannelSnippetBase):
    class Meta:
        unique_together = ['channel', 'snap_date']



class YoutubeChannelStatisticsBase(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.CASCADE, related_name="%(class)s")

    viewCount = models.BigIntegerField(verbose_name='viewCount' , null=True, blank=True)
    commentCount = models.BigIntegerField(verbose_name='commentCount' , null=True, blank=True)
    subscriberCount = models.BigIntegerField(verbose_name='subscriberCount' , null=True, blank=True)
    hiddenSubscriberCount = models.BooleanField(verbose_name='hiddenSubscriberCount' , null=True, blank=True)
    videoCount = models.BigIntegerField(verbose_name='videoCount' , null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "유튜브 채널 Statistics 정보"
        verbose_name_plural = "유튜브 채널 Statistics 정보"

class YoutubeChannelStatistics(YoutubeChannelStatisticsBase):
    pass

class YoutubeChannelStatisticsSnap(YoutubeChannelStatisticsBase):
    class Meta:
        unique_together = ['channel', 'snap_date']



class YoutubeThumbnails(YoutubeBaseModel):
    CHANNEL, VIDEO, SEARCH, PLAYLIST = (0,1,2,3)

    thumbnail_type = (
        (CHANNEL, 'Channel'),
        (VIDEO, 'Video'),
        (SEARCH, 'Search'),
        (PLAYLIST, 'Playlist')
    )

    type = models.IntegerField(null=True, blank=True, choices=thumbnail_type)

    #썸네일 기준으로 쿼리하기 위하여 역forienkey로 설계
    channel_snippet = models.ForeignKey('YoutubeChannelSnippet',verbose_name='채널 snippet', null=True, blank=True, related_name="thumbnails" , on_delete=models.SET_NULL)
    video_snippet = models.ForeignKey('YoutubeVideoSnippet',verbose_name='비디오 snippet', null=True, blank=True, related_name="thumbnails", on_delete=models.SET_NULL)
    result_snippet = models.ForeignKey('YoutubeSearchResult',verbose_name='결과 snippet', null=True, blank=True, related_name="thumbnails", on_delete=models.SET_NULL)
    playlist_snippet = models.ForeignKey('YoutubePlaylistSnippet',verbose_name='플레이리스트 snippet', null=True, blank=True, related_name="thumbnails", on_delete=models.SET_NULL)

    key = models.CharField(max_length=20, verbose_name='키값', null=True, blank=True, db_index=True)
    url = models.URLField(max_length=500, verbose_name='이미지',null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

class YoutubeChannelContentDetails(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.CASCADE)
    googlePlusUserId = models.CharField(max_length=70, verbose_name='UserId', null=True, blank=True)

class YoutubeChannelContentDetailsRelatedPlaylists(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, related_name="relatedPlaylists", on_delete=models.CASCADE)
    contentDetails = models.ForeignKey(YoutubeChannelContentDetails,verbose_name='채널', null=True, blank=True, related_name="relatedPlaylists", on_delete=models.CASCADE)
    playlist = models.ForeignKey('YoutubePlaylist',verbose_name='플레이리스트', null=True, blank=True, on_delete=models.SET_NULL, related_name="relatedplaylists")

    uploads = models.CharField(max_length=255, verbose_name='uploads', null=True, blank=True)
    likes = models.CharField(max_length=255, verbose_name='likes', null=True, blank=True)
    favorites = models.CharField(max_length=255, verbose_name='favorites', null=True, blank=True)
    watchHistory = models.CharField(max_length=255, verbose_name='watchHistory', null=True, blank=True)
    watchLater = models.CharField(max_length=255, verbose_name='watchLater', null=True, blank=True)

class YoutubeChannelStatus(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.CASCADE)
    privacyStatus = models.CharField(max_length=12, verbose_name='privacyStatus', null=True, blank=True)
    isLinked = models.BooleanField(verbose_name='isLinked', null=True, blank=True)

class YoutubeChannelBrandingSettings(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, related_name="brandingSettings", on_delete=models.CASCADE)


class YoutubeChannelBrandingSettingsChannel(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.CASCADE)
    brandingSettings = models.ForeignKey(YoutubeChannelBrandingSettings,verbose_name='채널', null=True, blank=True, related_name="brandsettingschannel", on_delete=models.CASCADE)

    title = models.CharField(max_length=255, verbose_name='타이틀', null=True, blank=True)
    description = models.CharField(max_length=255, verbose_name='설명', null=True, blank=True)
    keywords = models.CharField(max_length=255, verbose_name='키워드', null=True, blank=True)
    defaultTab = models.CharField(max_length=255, verbose_name='디폴트 탭', null=True, blank=True)
    trackingAnalyticsAccountId = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    moderateComments = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    showRelatedChannels = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    showBrowseView = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    featuredChannelsTitle = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    likes = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    featuredChannelsUrls = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    unsubscribedTrailer = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)
    profileColor = models.CharField(max_length=255, verbose_name='키값', null=True, blank=True)

class YoutubeTopicDetail(YoutubeBaseModel):
    topicCategories = models.CharField(max_length=255, verbose_name='토픽 카테고리', null=True, blank=True)
    topicId = models.CharField(max_length=50, verbose_name='토픽 아이디', default="null", unique=True)

    def __str__(self):
        if self.topicCategories != None:
            return '%s (%s)' % (self.topicCategories.replace('https://en.wikipedia.org/wiki/',''), self.topicId)
        else:
            return '%s' % (self.topicId)

class YoutubePlaylist(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.CASCADE, related_name="playlist")
    playlist_id = models.CharField(max_length=70, verbose_name='플레이 리스트 아이디', unique=True, default=0)

class YoutubePlaylistStatus(YoutubeBaseModel):
    playlist = models.ForeignKey(YoutubePlaylist,verbose_name='플레이리스트', null=True, blank=True, on_delete=models.SET_NULL, related_name="status")
    privacyStatus = models.CharField(max_length=12, verbose_name='privacyStatus', null=True, blank=True)
    isLinked = models.BooleanField(verbose_name='isLinked', null=True, blank=True)

class YoutubePlaylistSnippet(YoutubeBaseModel):
    playlist = models.ForeignKey(YoutubePlaylist,verbose_name='플레이리스트', null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s")
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s")
    channelTitle = models.CharField(max_length=255, verbose_name='채널명', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='플레이리스트명', null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name='플레이 리스트 설명', null=True, blank=True)
    publishedAt = models.DateTimeField(verbose_name='publishedAt', null=True, blank=True)



"""

유튜브 비디오 

"""
class YoutubeVideoManager(models.Manager):

    def get_queryset(self):
        qs = super(YoutubeVideoManager, self).get_queryset()
        return qs.select_related('snippet', 'statistics', 'contentDetails', 'status', 'recordingDetails')


class YoutubeVideo(YoutubeBaseModel):
    channel = models.ForeignKey(YoutubeChannel,verbose_name='채널', null=True, blank=True, related_name="videos", on_delete=models.SET_NULL)
    playlist = models.ForeignKey(YoutubePlaylist,verbose_name='플레이리스트', null=True, blank=True, related_name="videos", on_delete=models.SET_NULL)
    video_id = models.CharField(max_length=70, verbose_name='비디오 아이디', unique=True, default=0)

    topicDetails = models.ManyToManyField('YoutubeTopicDetail', blank=True, related_name="videos") #topicDetails.topicIds[]
    relevanttopicDetails  = models.ManyToManyField('YoutubeTopicDetail', blank=True, related_name="relevantvideos") # topicDetails.relevantTopicIds[]

    snippet = models.OneToOneField('YoutubeVideoSnippet',verbose_name='snippet', null=True, blank=True, on_delete=models.SET_NULL)
    statistics = models.OneToOneField('YoutubeVideoStatistics',verbose_name='statistics', null=True, blank=True, on_delete=models.SET_NULL)
    contentDetails = models.OneToOneField('YoutubeVideoContentDetails',verbose_name='contentDetails', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.OneToOneField('YoutubeVideoStatus',verbose_name='status', null=True, blank=True, on_delete=models.SET_NULL)
    recordingDetails = models.OneToOneField('YoutubeVideoRecordingDetails',verbose_name='recordingDetails', null=True, blank=True, on_delete=models.SET_NULL)

    '''
        피처링 모델
    '''
    transcript = models.OneToOneField('YoutubeVideoTranscript',verbose_name='transcript', null=True, blank=True, on_delete=models.SET_NULL)

    def get_channel_id(self):
        if self.channel == None:
            return None
        return self.channel.channel_id


    def get_title(self):
        try:
            return '%s' % self.snippet.title
        except:
            return None

    def get_description(self):
        try:
            return '%s' % self.snippet.description
        except:
            return None

    objects = YoutubeVideoManager()

    # def __str__(self):
    #     return '%s (%s)' % (self.get_title(), self.video_id)

class YoutubeVideoSnippetBase(YoutubeBaseModel):
    type_regions = {
        (0, '한국'),
        (1, '미국' ),
        (2, '영국' ),
    }
    video = models.ForeignKey(YoutubeVideo,verbose_name='비디오', null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s")

    title = models.CharField(max_length=255, verbose_name='비디오 명', null=True, blank=True)
    categoryId = models.CharField(max_length=10, verbose_name='카테고리 아이디', null=True, blank=True)
    channelId = models.CharField(max_length=70, verbose_name='채널 아이디', null=True, blank=True)
    playlistId = models.CharField(max_length=70, verbose_name='플레이 리스트 아이디', null=True, blank=True)
    channelTitle = models.CharField(max_length=255, verbose_name='채널 타이틀', null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name='비디오 설명', null=True, blank=True)
    publishedAt = models.DateTimeField(verbose_name='publishedAt', null=True, blank=True)
    defaultAudioLanguage = models.CharField(max_length=10, verbose_name='오디오 랭귀지', null=True, blank=True)
    defaultLanguage = models.CharField(max_length=10, verbose_name='랭귀지', null=True, blank=True)
    tags = models.ManyToManyField('YoutubeVideoTag',verbose_name='비디오', blank=True)

    def get_tags(self):
        return ','.join(str(v) for v in self.tags.all())

    def get_tags_list(self):
        return list(self.tags.values_list('name', flat=True))

    def __str__(self):
        if self.title == None:
            return '%s의 비디오' % self.channelId
        return '%s' % self.title

    class Meta:
        abstract=True
        verbose_name = "유튜브 비디오 정보"
        verbose_name_plural = "유튜브 비디오 정보"

class YoutubeVideoSnippet(YoutubeVideoSnippetBase):
    pass

class YoutubeVideoSnippetSnap(YoutubeVideoSnippetBase):
    class Meta:
        unique_together = ['video', 'snap_date']

class YoutubeVideoTag(YoutubeBaseModel):
    name = models.CharField(max_length=100, verbose_name='태그명', null=True, blank=True, unique=True)

    def __str__(self):
        return '%s' % self.name

class YoutubeVideoContentDetails(YoutubeBaseModel):
    video = models.ForeignKey(YoutubeVideo,verbose_name='비디오', null=True, blank=True, on_delete=models.CASCADE)
    duration = models.DurationField(verbose_name='재생 시간', null=True, blank=True)
    dimension = models.CharField(max_length=255, verbose_name='dimension', null=True, blank=True)
    caption = models.BooleanField(verbose_name='자막 유무' , default=False, null=True, blank=True)
    definition = models.CharField(max_length=10, verbose_name='영상 화질', null=True, blank=True)
    licensedContent = models.BooleanField(verbose_name='license Content' , default=False, null=True, blank=True)

class YoutubeVideoStatus(YoutubeBaseModel):
    video = models.ForeignKey(YoutubeVideo,verbose_name='비디오', null=True, blank=True, on_delete=models.CASCADE)
    uploadStatus = models.CharField(max_length=255, null=True, blank=True)
    failureReason = models.CharField(max_length=255, null=True, blank=True)
    rejectionReason = models.CharField(max_length=255, null=True, blank=True)
    privacyStatus = models.CharField(max_length=255, null=True, blank=True)
    license = models.CharField(max_length=255, null=True, blank=True)

    embeddable = models.BooleanField(default=False, null=True, blank=True)
    publicStatsViewable = models.BooleanField(default=False, null=True, blank=True)

class YoutubeVideoStatisticsBase(YoutubeBaseModel):
    video = models.ForeignKey(YoutubeVideo,verbose_name='비디오', null=True, blank=True,  on_delete=models.CASCADE, related_name="%(class)s")
    viewCount = models.BigIntegerField(verbose_name='viewCount' , null=True, blank=True)
    likeCount = models.BigIntegerField(verbose_name='likeCount' , null=True, blank=True)
    dislikeCount = models.BigIntegerField(verbose_name='dislikeCount' , null=True, blank=True)
    favoriteCount = models.BigIntegerField(verbose_name='favoriteCount' , null=True, blank=True)
    commentCount = models.BigIntegerField(verbose_name='commentCount' , null=True, blank=True)


    class Meta:
        abstract=True
        verbose_name = "유튜브 비디오 statistics 정보"
        verbose_name_plural = "유튜브 비디오 statistics 정보"

class YoutubeVideoStatistics(YoutubeVideoStatisticsBase):
    pass

class YoutubeVideoStatisticsSnap(YoutubeVideoStatisticsBase):
    class Meta:
        unique_together = ['video', 'snap_date']

class YoutubeVideoRecordingDetails(YoutubeBaseModel):
    video = models.ForeignKey(YoutubeVideo,verbose_name='비디오', null=True, blank=True, on_delete=models.CASCADE)
    locationDescription = models.CharField(max_length=255, null=True, blank=True)
    recordingDate = models.DateTimeField(verbose_name='recordingDate', null=True, blank=True)
    location = models.ForeignKey('YoutubeLocation', verbose_name='위치', null=True, blank=True, related_name="recordingDetails", on_delete=models.SET_NULL)

class YoutubeLocation(YoutubeBaseModel):
    latitude = models.FloatField(verbose_name='latitude' , null=True, blank=True)
    longitude = models.FloatField(verbose_name='longitude' , null=True, blank=True)
    altitude = models.FloatField(verbose_name='altitude' , null=True, blank=True)

    class Meta:
        unique_together = ('latitude', 'longitude', 'altitude')

class YoutubeVideoTranscript(BaseModel):
    """
        피처링 정의 모델
    """
    video_id = models.CharField(max_length=70, verbose_name='비디오 아이디', unique=True, default=0)
    language_code = models.CharField(max_length=20, null=True, blank=True)
    is_generated = models.BooleanField(default=False, null=True, blank=True)
    is_translatable = models.BooleanField(default=False, null=True, blank=True)
    transcript_count = models.IntegerField(null=True, blank=True)



"""

유튜브 댓글 

"""
class YoutubeCommentThread(YoutubeBaseModel):
    commentthread_id = models.CharField(max_length=70, verbose_name='댓글쓰레드 아이디', unique=True, default=0)
    channel = models.ForeignKey('YoutubeChannel',verbose_name='채널', null=True, blank=True, related_name="commentthread", on_delete=models.SET_NULL)
    video = models.ForeignKey('YoutubeVideo',verbose_name='비디오', null=True, blank=True, related_name="commentthread", on_delete=models.SET_NULL)

    snippet = models.OneToOneField('YoutubeCommentThreadSnippet',verbose_name='snippet', null=True, blank=True, on_delete=models.SET_NULL)

class YoutubeCommentThreadSnippetBase(YoutubeBaseModel):
    commentthread = models.ForeignKey(YoutubeCommentThread, null=True, blank=True, on_delete=models.CASCADE)

    canReply = models.BooleanField(default=False, null=True, blank=True)
    isPublic = models.BooleanField(default=False, null=True, blank=True)
    topLevelComment = models.ForeignKey('YoutubeComment',verbose_name='탑 댓글', null=True, blank=True, on_delete=models.SET_NULL)
    totalReplyCount = models.BigIntegerField(verbose_name='totalReplyCount' , null=True, blank=True)
    videoId = models.CharField(max_length=70, null=True, blank=True)

    class Meta:
        abstract = True

class YoutubeCommentThreadSnippet(YoutubeCommentThreadSnippetBase):
    pass

# class YoutubeCommentThreadSnippetBase(YoutubeCommentThreadSnippetBase):
#     class Meta:
#         unique_together = ['channel', 'snap_date']


class YoutubeComment(YoutubeBaseModel):
    comment_id = models.CharField(max_length=70, verbose_name='댓글 아이디', unique=True, default=0)
    
    snippet = models.OneToOneField('YoutubeCommentSnippet',verbose_name='snippet', null=True, blank=True, on_delete=models.SET_NULL)

    '''
        피처링 연결 모델
    '''
    channel = models.ForeignKey('YoutubeChannel',verbose_name='채널', null=True, blank=True, related_name="comment", on_delete=models.SET_NULL)
    video = models.ForeignKey('YoutubeVideo',verbose_name='비디오', null=True, blank=True, related_name="comment", on_delete=models.SET_NULL)
    thread = models.ForeignKey(YoutubeCommentThread,verbose_name='댓글 쓰레드', null=True, blank=True, related_name="replies_comments", on_delete=models.SET_NULL)

    def get_channel_id(self):
        if self.channel == None:
            return None
        return self.channel.channel_id

class YoutubeCommentSnippetBase(YoutubeBaseModel):
    '''
        피처링 연결 모델
    '''
    comment = models.ForeignKey(YoutubeComment, null=True, blank=True, on_delete=models.CASCADE, related_name="%(class)s")
    author_channel = models.ForeignKey('YoutubeChannel',verbose_name='글쓴이 채널', null=True, blank=True, related_name="author_comment", on_delete=models.SET_NULL)

    moderationStatus = models.CharField(max_length=30, null=True, blank=True)
    authorChannelId = models.CharField(max_length=70, null=True, blank=True)
    authorChannelUrl = models.CharField(max_length=500, null=True, blank=True)
    authorDisplayName = models.CharField(max_length=120, null=True, blank=True)
    authorProfileImageUrl = models.CharField(max_length=500, null=True, blank=True)
    canRate = models.BooleanField(default=False, null=True, blank=True)
    likeCount = models.BigIntegerField(verbose_name='viewCount' , null=True, blank=True)
    publishedAt = models.DateTimeField(verbose_name='publishedAt', null=True, blank=True)
    textDisplay = models.TextField(null=True, blank=True)
    textOriginal = models.TextField(null=True, blank=True)
    updatedAt = models.DateTimeField(verbose_name='updatedAt', null=True, blank=True)
    videoId = models.CharField(max_length=70, null=True, blank=True)
    viewerRating = models.CharField(max_length=20, null=True, blank=True)

    def get_channel_id(self):
        return self.comment.get_channel_id()

    class Meta:
        abstract = True

class YoutubeCommentSnippet(YoutubeCommentSnippetBase):
    pass