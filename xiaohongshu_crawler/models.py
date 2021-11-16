from django.db import models
from django.utils.timezone import now
import traceback


class XiaCrawlRecord(models.Model):
    """모든 크롤링된 데이터들은 해당 레코드를 참조하고 있어야한다.

        Attribute:
            from_source : 어디서 수집 되었는지 나타내는 Enum
    """

    from_source_type = {
        (0, 'Featuring Lambda'),  # 서버 외부의 우리 람다 서버에서
        (1, 'Featuring Request'),  # 서버 내에 리퀘스트 통해
        (2, 'Other API'),  # 99API등 타사 API를 통해
    }

    from_source = models.IntegerField(default=0, blank=True, choices=from_source_type)
    crawl_type = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='인스타 크롤링 시간', auto_now_add=True, blank=True)


class BaseModel(models.Model):
    """모든 크롤링된 데이터들 클래스는 해당 Base를 상속 받아야 한다.

    """

    record = models.ForeignKey(XiaCrawlRecord, on_delete=models.SET_NULL, verbose_name='크롤링 레코드', null=True, blank=True, related_name="%(class)s")
    created_time = models.DateTimeField(verbose_name='생성 시간', default=now, blank=True)
    updated_time = models.DateTimeField(verbose_name='수정 시간', default=now, blank=True)
    snap_time = models.DateTimeField(verbose_name='스냅 생성 시간', default=now, blank=True)
    snap_date = models.DateField(verbose_name='스냅 생성 날짜', default=now, blank=True)

    def save(self, *args, **kwargs):
        self.updated_time = now()
        try:
            super(BaseModel, self).save()
        except:
            print('save error : ', self.__class__.__name__, traceback.format_exc())
            pass

    def jsonToClass(self, json):
        for key, value in json.items():
            try:
                # if hasattr(self, 'insta_pk') and ('pk' == key or 'insta_pk' == key):
                #     self.insta_pk = value
                # elif hasattr(self, 'created_at') and 'created_at' == key:
                #     self.created_at = datetime.fromtimestamp(value)
                # elif hasattr(self, 'taken_at') and 'taken_at' == key:
                #     utc_timezone = timezone.utc
                #     self.taken_at = datetime.fromtimestamp(value, utc_timezone)
                # elif hasattr(self, 'hd_profile_pic_url_info') and 'hd_profile_pic_url_info' == key:
                #     if 'url' in value:
                #         self.hd_profile_pic_url = value['url']
                # elif hasattr(self, 'insta_id') and 'id' == key:
                #     self.insta_id = value
                # elif hasattr(self, key):
                #     setattr(self, key, value)
                pass
            except:
                # print('set attr : ', traceback.format_exc())
                pass

    class Meta:
        abstract = True


"""

Board

"""
class XiaCrawlBoardBase(BaseModel):
    user = models.ForeignKey('XiaCrawlProfile', on_delete=models.SET_NULL, verbose_name='앨범 제작자 이름', null=True)

    board_id = models.CharField(max_length=200, verbose_name='앨범 ID')
    is_enabled = models.BooleanField(default=False, verbose_name='공개여부')
    desc = models.TextField(null=True)
    name = models.CharField(max_length=100, verbose_name='앨범 이름')

    noteCount = models.IntegerField(default=0, verbose_name='앨범 포스트 수')
    fanCount = models.IntegerField(default=0, verbose_name='앨범 구독자 수')
    notes = models.ManyToManyField('CrawlNote')

    class Meta:
        abstract = True


class XiaCrawlBoard(XiaCrawlBoardBase):
    pass

    class Meta:
        verbose_name = "앨범"
        verbose_name_plural = "앨범 정보"


class XiaCrawlBoardSnapshot(XiaCrawlBoardBase):
    pass

    class Meta:
        unique_together = ['board_id', 'snap_date']

"""

Note

"""


# 노트 카테고리
class XiaCrawlNoteCategoriesBase(BaseModel):
    name = models.CharField(max_length=100, verbose_name='카테고리 이름', null=True)
    categoriesIndex = models.IntegerField(verbose_name='카테고리 인덱스')


class XiaCrawlNoteMainCategories(XiaCrawlNoteCategoriesBase):
    korea = models.CharField(max_length=100, verbose_name='메인 카테고리 한글', null=True)

    class Meta:
        verbose_name = "노트 메인 카테고리"
        verbose_name_plural = "노트 메인 카테고리 정보"


class XiaCrawlNoteSubCategories(XiaCrawlNoteCategoriesBase):
    mainCategory = models.ForeignKey(XiaCrawlNoteMainCategories, on_delete=models.SET_NULL, verbose_name='대분류', null=True)

    class Meta:
        verbose_name = "노트 서브 카테고리"
        verbose_name_plural = "노트 서브 카테고리 정보"





# 노트 키워드
class XiaCrawlNoteKeyword(BaseModel):
    keyword_name = models.CharField(max_length=100, verbose_name='키워드 이름')
    keyword_id = models.CharField(max_length=50, verbose_name='키워드 아이디')

    class Meta:
        verbose_name = "노트 키워드"
        verbose_name_plural = "노트 키워드 정보"


class CrawlNoteKeywordRelated(BaseModel):
    targetKeyword = models.OneToOneField(XiaCrawlNoteKeyword, on_delete=models.SET_NULL, verbose_name='대상 키워드', null=True, blank=True)
    relatedKeyword = models.ManyToManyField(XiaCrawlNoteKeyword, verbose_name='연관 키워드', related_name='note_keyword_related')

    class Meta:
        verbose_name = "노트 연관 키워드"
        verbose_name_plural = "노트 연관 키워드 정보"





# 노트
class CrawlNoteBase(BaseModel):
    TYPE_NOTE = (
        (0, 'image'),
        (1, 'video'),
    )

    type = models.IntegerField(choices=TYPE_NOTE, default=0)
    note_id = models.CharField(max_length=40, null=True, blank=True)

    user = models.ForeignKey('XiaCrawlProfile', on_delete=models.SET_NULL, verbose_name='크롤링된 프로필', null=True)
    category = models.ForeignKey('XiaCrawlNoteSubCategories', on_delete=models.SET_NULL, verbose_name='카테고리 정보', null=True)
    keywords = models.ManyToManyField('XiaCrawlNoteKeyword', verbose_name='키워드 정보', related_name="%(class)s")

    likes = models.BigIntegerField(verbose_name='좋아요 갯수', null=True, blank=True, default=0)
    collects = models.BigIntegerField(verbose_name='북마크 갯수', null=True, blank=True, default=0)
    shareCount = models.BigIntegerField(verbose_name='공유 갯수', null=True, blank=True, default=0)
    comments = models.BigIntegerField(verbose_name='댓글 갯수', null=True, blank=True, default=0)

    time = models.DateTimeField(verbose_name='작성 시간', null=True, blank=True)

    class Meta:
        abstract = True


class CrawlNoteSnapshot(CrawlNoteBase):
    pass

    class Meta:
        unique_together = ['note_id', 'snap_date']


class CrawlNote(CrawlNoteBase):
    pass
    def __str__(self):
        return '노트(%s)' % (self.note_id)

    class Meta:
        verbose_name = "노트"
        verbose_name_plural = "노트 정보"





# 노트 글내용
class CrawlNoteCaptionBase(BaseModel):
    note = models.ForeignKey('CrawlNote', on_delete=models.SET_NULL, verbose_name='크롤링된 노트', null=True, blank=True)

    title = models.CharField(max_length=300)
    desc = models.TextField(null=True)

    class Meta:
        abstract = True


class CrawlNoteCaption(CrawlNoteCaptionBase):
    pass
    def __str__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name = "노트 글내용"
        verbose_name_plural = "노트 글내용 정보"





# 연관 노트
class CrawlNoteRelated(BaseModel):
    targetNote = models.OneToOneField('CrawlNote', on_delete=models.SET_NULL, verbose_name='대상 노트', null=True, blank=True)
    relatedNote = models.ManyToManyField('CrawlNote', verbose_name='연관 노트', related_name='note')

    class Meta:
        verbose_name = "연관 노트"
        verbose_name_plural = "연관 노트 정보"





# 노트 이미지
class CrawlNoteImage(BaseModel):
    COVER_TYPE = 0
    SUB_TYPE = 1
    TYPE_IMAGE = (
        (COVER_TYPE, 'cover'),
        (SUB_TYPE, 'sub'),
    )

    cover = models.IntegerField(verbose_name='이미지 타입', choices=TYPE_IMAGE, default=0)
    url = models.URLField(max_length=500, verbose_name='미디어 URL', null=True, blank=True)
    width = models.IntegerField(verbose_name='가로길이', null=True, blank=True)
    height = models.IntegerField(verbose_name='세로길이', null=True, blank=True)
    fileId = models.CharField(verbose_name='파일ID', max_length=200)

    class Meta:
        verbose_name = "노트 미디어"
        verbose_name_plural = "노트 미디어 정보"


# 노트 캐러셀
class CrawlCarouselMedia(BaseModel):
    note = models.ForeignKey(CrawlNote, on_delete=models.SET_NULL, verbose_name='크롤링된 캐러셀', null=True, blank=True)
    detail_image = models.ManyToManyField(CrawlNoteImage, verbose_name='미디어', related_name='note_image')

    class Meta:
        verbose_name = "노트 캐러셀"
        verbose_name_plural = "노트 캐러셀 정보"





# 노트 댓글
class CrawlNoteCommentsBase(BaseModel):
    comments_id = models.CharField(max_length=200, verbose_name='댓글 ID')
    user = models.ForeignKey('XiaCrawlProfile', on_delete=models.SET_NULL, verbose_name='댓글 작성자', null=True, blank=True)

    content = models.TextField(verbose_name='내용')
    likes = models.BigIntegerField(verbose_name='좋아요 갯수', null=True, blank=True, default=0)

    time = models.DateTimeField(verbose_name='작성 시간', null=True, blank=True)


class CrawlNoteSubComments(CrawlNoteCommentsBase):
    targetCommentId = models.CharField(max_length=200, verbose_name='대상 댓글', null=True, blank=True)

    class Meta:
        verbose_name = "노트 대댓글"
        verbose_name_plural = "노트 대댓글 정보"


class CrawlNoteComments(CrawlNoteCommentsBase):
    targetNoteId = models.ForeignKey(CrawlNote, on_delete=models.SET_NULL, verbose_name='대상 노트', null=True, blank=True)

    subCommentsTotal = models.IntegerField(verbose_name='대댓글 갯수', default=0)
    subComments = models.ManyToManyField(CrawlNoteSubComments, verbose_name='대댓글', related_name='note_sub_comments')

    class Meta:
        verbose_name = "노트 댓글"
        verbose_name_plural = "노트 댓글 정보"


"""

Profile

"""

class XiaCrawlProfileImage(BaseModel):
    bannerImage = models.URLField(max_length=500, verbose_name='샤오홍슈 배너 이미지', null=True, blank=True)
    image = models.URLField(max_length=500, verbose_name='샤오홍슈 프로필 이미지', null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)


class XiaCrawlProfileLevel(BaseModel):
    name = models.CharField(max_length=100, verbose_name='레벨 이름')
    image = models.URLField(max_length=500, verbose_name='레벨 이미지')

    def __str__(self):
        return '%s' % (self.name)

class XiaCrawlProfileBase(BaseModel):
    USER_GENDER = (
        (0, '남성'),
        (1, '여성'),
        (2, '알수없음'),
    )

    is_profile_crawled = models.BooleanField(verbose_name='샤오홍슈 프로필 크롤링 유무', default=False)
    is_analy_requirements = models.BooleanField(verbose_name='샤오홍슈 프로필 분석 기본 조건 충족', default=False)
    is_analy_complete = models.BooleanField(verbose_name='유저 분석 유무', default=False)
    is_report_complete = models.BooleanField(verbose_name='리포트 생성 유무', default=False)

    image = models.OneToOneField(XiaCrawlProfileImage, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.CharField(max_length=200, verbose_name='샤오홍슈 유저 아이디')
    nickname = models.CharField(max_length=200, verbose_name='샤오홍슈 유저 닉네임')
    desc = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name='위치', null=True, blank=True)

    gender = models.IntegerField(choices=USER_GENDER, default=2)
    fans = models.IntegerField(verbose_name='팔로워 수', default=0)
    follows = models.IntegerField(verbose_name='팔로잉 수', default=0)
    notes = models.IntegerField(verbose_name='노트 수', default=0)
    boards = models.IntegerField(verbose_name='앨범 갯수', default=0)
    liked = models.IntegerField(verbose_name='좋아요 수', default=0)
    collected = models.IntegerField(verbose_name='북마크 수', default=0)

    level = models.ForeignKey(XiaCrawlProfileLevel, verbose_name='유저 레벨', on_delete=models.SET_NULL, null=True, blank=True)

    officialVerified = models.BooleanField(verbose_name='오피셜 인증 유무', default=False)
    redOfficialVerifyType = models.IntegerField(default=0)
    redOfficialVerifyShowIcon = models.BooleanField(default=False)
    redOfficialVerifyIconType = models.IntegerField(default=0)

    class Meta:
        abstract = True


class CrawlUserProfileSnapshot(XiaCrawlProfileBase):
    class Meta:
        unique_together = ['user_id', 'snap_date']


class XiaCrawlProfile(XiaCrawlProfileBase):
    pass
    def __str__(self):
        return '프로필(%s)' % (self.user_id)


class XiaCrawlProfileRelation(BaseModel):
    targetProfile = models.ForeignKey(XiaCrawlProfile, verbose_name='팔로워 받은 대상', on_delete=models.SET_NULL, null=True, related_name='target_follower_profile')
    followingProfile = models.ForeignKey(XiaCrawlProfile, verbose_name='팔로잉 유저', on_delete=models.SET_NULL, null=True, related_name='following_profile')



class CrawlUserProfileProxy(XiaCrawlProfile):
    class Meta:
        proxy = True
        verbose_name = "샤오홍슈 인플루언서 프로필"
        verbose_name_plural = "샤오홍슈 인플루언서 프로필 정보"
