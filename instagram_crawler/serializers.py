from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from instagram_crawler.models import CrawlRecord, CrawlProfileImage, CrawlUserProfileSnapshot, CrawlUserProfile, CrawlPostSnapshot, CrawlPost, CrawlPostCaption, CrawlPostLiker, CrawlUserSimilar, CrawlUserFollower, CrawlPostLikerProxy, CrawlUserProfileProxy, CrawlUserFollowerProxy, CrawlCarouselMedia, CrawlPostImageVersion2Candidate, CrawlPostVideoVersion, CrawlPostComment, CrawlPostLocation, CrawlPostUserTags, CrawlSearchTagRelatedPost, CrawlRelatedTag, CrawlSearchTag, CrawlSearchTagSnapshot, CrawlSearchTagProxy, CrawlLocationRelatedPost, CrawlLocationFeed, CrawlLocationFeedSnapshot


class CrawlRecordSerializer(ModelSerializer):

    class Meta:
        model = CrawlRecord
        fields = '__all__'


class CrawlProfileImageSerializer(ModelSerializer):

    class Meta:
        model = CrawlProfileImage
        fields = '__all__'


class CrawlUserProfileSnapshotSerializer(ModelSerializer):

    class Meta:
        model = CrawlUserProfileSnapshot
        # fields = '__all__'
        fields = ('insta_pk', 'username','full_name', 'biography', 'media_count', 'following_count', 'follower_count', 'public_phone_number', 'public_email', 'external_url', 'snap_date', 'updated_time')


class CrawlUserProfileSerializer(ModelSerializer):

    class Meta:
        model = CrawlUserProfile
        fields = '__all__'


class CrawlPostSnapshotSerializer(ModelSerializer):

    class Meta:
        model = CrawlPostSnapshot
        fields = '__all__'


class CrawlPostCaptionSerializer(ModelSerializer):

    class Meta:
        model = CrawlPostCaption
        fields = '__all__'


class CrawlPostSerializer(ModelSerializer):
    # crawlpostcaption = CrawlPostCaptionSerializer(many=True, read_only=True)
    crawlpostcaption = SerializerMethodField()
    thumbnail = SerializerMethodField()

    def get_thumbnail(self,obj):
        try:
            image = obj.get_image()
            return image.url
        except:
            return None

    def get_crawlpostcaption(self,obj):
        caption = obj.crawlpostcaption.exclude(text=None).all()[:2]
        serializer = CrawlPostCaptionSerializer(caption, many=True)
        return serializer.data

    class Meta:
        model = CrawlPost
        fields = '__all__'


class CrawlPostLikerSerializer(ModelSerializer):

    class Meta:
        model = CrawlPostLiker
        fields = '__all__'


class CrawlUserSimilarSerializer(ModelSerializer):
    user = CrawlUserProfileSnapshotSerializer(many=False)

    class Meta:
        model = CrawlUserSimilar
        exclude = ('id', 'created_time', 'snap_time', 'record', 'target_user')


class CrawlUserFollowerSerializer(ModelSerializer):
    user = CrawlUserProfileSnapshotSerializer(many=False)

    class Meta:
        model = CrawlUserFollower
        exclude = ('id', 'created_time', 'snap_time', 'record', 'target_user')


class CrawlPostLikerProxySerializer(ModelSerializer):

    class Meta:
        model = CrawlPostLikerProxy
        fields = '__all__'


class CrawlUserProfileProxySerializer(ModelSerializer):

    class Meta:
        model = CrawlUserProfileProxy
        fields = '__all__'


class CrawlUserFollowerProxySerializer(ModelSerializer):

    class Meta:
        model = CrawlUserFollowerProxy
        fields = '__all__'


class CrawlCarouselMediaSerializer(ModelSerializer):

    class Meta:
        model = CrawlCarouselMedia
        fields = '__all__'


class CrawlPostImageVersion2CandidateSerializer(ModelSerializer):

    class Meta:
        model = CrawlPostImageVersion2Candidate
        fields = '__all__'


class CrawlPostVideoVersionSerializer(ModelSerializer):

    class Meta:
        model = CrawlPostVideoVersion
        fields = '__all__'


class CrawlPostCommentSerializer(ModelSerializer):
    user = CrawlUserProfileSnapshotSerializer()
    
    class Meta:
        model = CrawlPostComment
        fields = '__all__'


class CrawlPostLocationSerializer(ModelSerializer):

    class Meta:
        model = CrawlPostLocation
        fields = '__all__'


class CrawlPostUserTagsSerializer(ModelSerializer):
    post = CrawlPostSerializer()
    user = CrawlUserProfileSerializer()

    class Meta:
        model = CrawlPostUserTags
        fields = '__all__'


class CrawlRelatedTagSerializer(ModelSerializer):

    class Meta:
        model = CrawlRelatedTag
        fields = '__all__'


class CrawlSearchTagSerializer(ModelSerializer):

    class Meta:
        model = CrawlSearchTag
        fields = ('name', 'media_count')

class CrawlSearchTagRelatedPostSerializer(ModelSerializer):
    post = CrawlPostSerializer()
    searchtag = CrawlSearchTagSerializer()

    class Meta:
        model = CrawlSearchTagRelatedPost
        fields = '__all__'



class CrawlSearchTagSnapshotSerializer(ModelSerializer):

    class Meta:
        model = CrawlSearchTagSnapshot
        fields = '__all__'


class CrawlSearchTagProxySerializer(ModelSerializer):

    class Meta:
        model = CrawlSearchTagProxy
        fields = '__all__'


class CrawlLocationRelatedPostSerializer(ModelSerializer):

    class Meta:
        model = CrawlLocationRelatedPost
        fields = '__all__'


class CrawlLocationFeedSerializer(ModelSerializer):

    class Meta:
        model = CrawlLocationFeed
        fields = '__all__'


class CrawlLocationFeedSnapshotSerializer(ModelSerializer):

    class Meta:
        model = CrawlLocationFeedSnapshot
        fields = '__all__'
