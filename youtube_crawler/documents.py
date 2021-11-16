from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import Text, Float, Boolean, Keyword
from elasticsearch_dsl import Document as DSLDocument

from django_elasticsearch_dsl.registries import registry
from .models import YoutubeChannel, YoutubeCommentSnippet, YoutubeVideo
from django.db.models import Prefetch

@registry.register_document
class YoutubeChannelDocument(Document):
    channelId = fields.TextField(attr="channel_id")
    title = fields.TextField(attr="get_title")
    description = fields.TextField(attr="get_description")

    snippet = fields.ObjectField(properties={
        'publishedAt': fields.DateField()
    })

    statistics = fields.ObjectField(properties={
        'viewCount': fields.DoubleField(),
        'commentCount': fields.DoubleField(),
        'subscriberCount': fields.DoubleField(), #위로도 옮김
        'hiddenSubscriberCount': fields.BooleanField(),
        'videoCount': fields.DoubleField()
    })

    class Index:
        name = 'youtubechannel'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = YoutubeChannel
        fields = ['id', 'channel_id']

    def get_queryset(self):
        return super(YoutubeChannelDocument, self).get_queryset().select_related(
            'snippet', 'statistics'
        )


@registry.register_document
class YoutubeVideoDocument(Document):
    videoId = fields.TextField(attr="video_id")
    title = fields.TextField(attr="get_title")
    description = fields.TextField(attr="get_description")
    channelId = fields.TextField(attr="get_channel_id")

    snippet = fields.ObjectField(properties={
        'channelId': fields.TextField(),
        'channelTitle': fields.TextField(),
        'publishedAt': fields.DateField(),
        'tags': fields.TextField(attr="get_tags")
    })

    statistics = fields.ObjectField(properties={
        'viewCount': fields.DoubleField(),
        'likeCount': fields.DoubleField(),
        'dislikeCount': fields.DoubleField(),
        'favoriteCount': fields.DoubleField(),
        'commentCount': fields.DoubleField()
    })

    class Index:
        name = 'youtubevideo'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = YoutubeVideo
        fields = ['id']

    def get_queryset(self):
        return super(YoutubeVideoDocument, self).get_queryset().select_related(
            'snippet', 'statistics'
        )



class YoutubeVideoTranscriptDocument(DSLDocument):
    channel_id = Text()
    video_id = Text()
    language_code = Text()
    is_generated = Boolean()
    is_translatable = Boolean()
    text = Text()
    start = Float()
    duration = Float()

    def parse_transcript_api(self, transcriptinfo, transcriptitem):
        self.video_id = transcriptinfo.video_id
        self.language_code = transcriptinfo.language_code
        self.is_generated = transcriptinfo.is_generated
        self.is_translatable = transcriptinfo.is_translatable

        self.text = transcriptitem['text']
        self.start = transcriptitem['start']
        self.duration = transcriptitem['duration']


    def save(self, using=None, index=None, validate=True, skip_empty=True, **kwargs):
        super(YoutubeVideoTranscriptDocument,self).save(using=using, index=index, validate=validate, skip_empty=skip_empty, **kwargs)

    class Index:
        name = 'youtubevideotranscript'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

@registry.register_document
class YoutubeCommentSnippetDocument(Document):

    channelId = fields.TextField(attr="get_channel_id")

    class Index:
        name = 'youtubecommentsnippet'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = YoutubeCommentSnippet
        fields = ['id', 'authorChannelId', 'authorDisplayName', 'authorProfileImageUrl', 'likeCount', 'publishedAt', 'textOriginal', 'updatedAt', 'videoId']

    def get_queryset(self):
        return super(YoutubeCommentSnippetDocument, self).get_queryset().select_related(
            'comment'
        )
