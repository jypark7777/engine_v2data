from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import CrawlUserProfile, CrawlPost, CrawlPostCaption, CrawlPostComment
from django.db.models import Prefetch

QUERY_START = 0
QUERY_END = QUERY_START+10000

@registry.register_document
class CrawlUserProfileDocument(Document):

    class Index:
        name = 'crawluserprofile'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = CrawlUserProfile
        fields = ['id', 'insta_pk', 'username', 'full_name', 'follower_count', 'following_count', 'media_count', 'usertags_count', 'biography', 'profile_pic_url', 'public_phone_number', 'public_email', 'external_url']

    def get_queryset(self, start_index=QUERY_START, end_index=None):
        if end_index == None:
            end_index = QUERY_END
        return super(CrawlUserProfileDocument, self).get_queryset()[start_index:end_index]

@registry.register_document
class CrawlPostDocument(Document):

    user = fields.ObjectField(properties={
        'insta_pk': fields.DoubleField(),
        'username' : fields.TextField(),
        'follower_count' : fields.IntegerField(),
    })
    is_sidecar_child = fields.BooleanField(attr='is_sidecar_child')

    text = fields.TextField(attr='get_caption_text_document')

    class Index:
        name = 'crawlpost'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = CrawlPost
        fields = ['id', 'insta_id', 'code', 'taken_at', 'like_count', 'comment_count', 'video_view_count', 'accessibility_caption']

    def get_queryset(self, start_index=QUERY_START, end_index=None):
        if end_index == None:
            end_index = QUERY_END
        queryset = CrawlPostCaption.objects.exclude(text=None).only('text')
        text_prefetch = Prefetch('crawlpostcaption', queryset=queryset)
        return super(CrawlPostDocument, self).get_queryset().select_related(
            'user'
            ).prefetch_related(
            text_prefetch
        )[start_index:end_index]

@registry.register_document
class CrawlPostCommentDocument(Document):
    post = fields.ObjectField(properties={
        'id': fields.DoubleField(),
        'insta_pk': fields.DoubleField(),
        'user_id': fields.DoubleField(),
        'taken_at' : fields.DateField()
    })

    user = fields.ObjectField(properties={
        'insta_pk': fields.DoubleField(),
        'username' : fields.TextField(),
    })


    class Index:
        name = 'crawlpostcomment'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = CrawlPostComment
        fields = ['insta_pk', 'text', 'created_at']

    def get_queryset(self,start_index=QUERY_START, end_index=None):
        if end_index == None:
            end_index = QUERY_END

        return super(CrawlPostCommentDocument, self).get_queryset().select_related(
        'user'
        ).prefetch_related(
            'post'
        )[start_index:end_index]