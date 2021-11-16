from re import search
from django.db.models.expressions import OuterRef
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from instagram_crawler.serializers import CrawlRecordSerializer, CrawlProfileImageSerializer, CrawlUserProfileSnapshotSerializer, CrawlUserProfileSerializer, CrawlPostSnapshotSerializer, CrawlPostSerializer, CrawlPostCaptionSerializer, CrawlPostLikerSerializer, CrawlUserSimilarSerializer, CrawlUserFollowerSerializer, CrawlPostLikerProxySerializer, CrawlUserProfileProxySerializer, CrawlUserFollowerProxySerializer, CrawlCarouselMediaSerializer, CrawlPostImageVersion2CandidateSerializer, CrawlPostVideoVersionSerializer, CrawlPostCommentSerializer, CrawlPostLocationSerializer, CrawlPostUserTagsSerializer, CrawlSearchTagRelatedPostSerializer, CrawlRelatedTagSerializer, CrawlSearchTagSerializer, CrawlSearchTagSnapshotSerializer, CrawlSearchTagProxySerializer, CrawlLocationRelatedPostSerializer, CrawlLocationFeedSerializer, CrawlLocationFeedSnapshotSerializer
from instagram_crawler.models import CrawlRecord, CrawlProfileImage, CrawlUserProfileSnapshot, CrawlUserProfile, CrawlPostSnapshot, CrawlPost, CrawlPostCaption, CrawlPostLiker, CrawlUserSimilar, CrawlUserFollower, CrawlPostLikerProxy, CrawlUserProfileProxy, CrawlUserFollowerProxy, CrawlCarouselMedia, CrawlPostImageVersion2Candidate, CrawlPostVideoVersion, CrawlPostComment, CrawlPostLocation, CrawlPostUserTags, CrawlSearchTagRelatedPost, CrawlRelatedTag, CrawlSearchTag, CrawlSearchTagSnapshot, CrawlSearchTagProxy, CrawlLocationRelatedPost, CrawlLocationFeed, CrawlLocationFeedSnapshot
from django.db.models import Count, Q, Subquery

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 10000

class BaseAPIView(APIView):
    pass

# class CrawlRecordAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlRecord.objects.get(pk=id)
#             serializer = CrawlRecordSerializer(item)
#             return Response(serializer.data)
#         except CrawlRecord.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlRecord.objects.get(pk=id)
#         except CrawlRecord.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlRecordSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlRecord.objects.get(pk=id)
#         except CrawlRecord.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlRecordAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlRecord.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlRecordSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlRecordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlProfileImageAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlProfileImage.objects.get(pk=id)
#             serializer = CrawlProfileImageSerializer(item)
#             return Response(serializer.data)
#         except CrawlProfileImage.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlProfileImage.objects.get(pk=id)
#         except CrawlProfileImage.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlProfileImageSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlProfileImage.objects.get(pk=id)
#         except CrawlProfileImage.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlProfileImageAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlProfileImage.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlProfileImageSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlProfileImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class CrawlUserProfileSnapshotAPIView(BaseAPIView):

    def get(self, request, user_id, format=None):
        try:
            item = CrawlUserProfileSnapshot.objects.filter(insta_pk=user_id).last()
            serializer = CrawlUserProfileSnapshotSerializer(item)
            return Response(serializer.data)
        except CrawlUserProfileSnapshot.DoesNotExist:
            return Response(status=404)

    # def put(self, request, id, format=None):
    #     try:
    #         item = CrawlUserProfileSnapshot.objects.get(pk=id)
    #     except CrawlUserProfileSnapshot.DoesNotExist:
    #         return Response(status=404)
    #     serializer = CrawlUserProfileSnapshotSerializer(item, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=400)

    # def delete(self, request, id, format=None):
    #     try:
    #         item = CrawlUserProfileSnapshot.objects.get(pk=id)
    #     except CrawlUserProfileSnapshot.DoesNotExist:
    #         return Response(status=404)
    #     item.delete()
    #     return Response(status=204)


class CrawlUserProfileSnapshotAPIListView(BaseAPIView):

    def get(self, request, user_id, format=None):
        items = CrawlUserProfileSnapshot.objects.filter(insta_pk=user_id).order_by('-snap_date')
        paginator = LargeResultsSetPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlUserProfileSnapshotSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlUserProfileSnapshotSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class CrawlUserProfileAPIView(BaseAPIView):

    def get(self, request, user_id, format=None):
        try:
            item = CrawlUserProfile.objects.get(insta_pk=user_id)
            serializer = CrawlUserProfileSerializer(item)
            return Response(serializer.data)
        except CrawlUserProfile.DoesNotExist:
            return Response(status=404)

class CrawlUserProfileUsernameAPIView(BaseAPIView):

    def get(self, request, username, format=None):
        try:
            item = CrawlUserProfile.objects.filter(username=username).last()
            if item == None:
                return Response(status=404)
            serializer = CrawlUserProfileSerializer(item)
            return Response(serializer.data)
        except CrawlUserProfile.DoesNotExist:
            return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlUserProfile.objects.get(pk=id)
#         except CrawlUserProfile.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlUserProfileSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlUserProfile.objects.get(pk=id)
#         except CrawlUserProfile.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlUserProfileAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlUserProfile.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlUserProfileSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlUserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostSnapshotAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostSnapshot.objects.get(pk=id)
#             serializer = CrawlPostSnapshotSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostSnapshot.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostSnapshot.objects.get(pk=id)
#         except CrawlPostSnapshot.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostSnapshotSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostSnapshot.objects.get(pk=id)
#         except CrawlPostSnapshot.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostSnapshotAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostSnapshot.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostSnapshotSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostSnapshotSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class CrawlPostAPIView(BaseAPIView):

    def get(self, request, code, format=None):
        try:
            item = CrawlPost.objects.get(code=code)
            serializer = CrawlPostSerializer(item)
            return Response(serializer.data)
        except CrawlPost.DoesNotExist:
            return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPost.objects.get(pk=id)
#         except CrawlPost.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPost.objects.get(pk=id)
#         except CrawlPost.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


class CrawlPostAPIListView(BaseAPIView):

    def get(self, request, user_id, format=None):
        items = CrawlPost.objects.filter(user__insta_pk=user_id, sidecar_parent__isnull=True).order_by('-insta_pk').distinct('insta_pk')
        paginator = LargeResultsSetPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        

#     def post(self, request, format=None):
#         serializer = CrawlPostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

class CrawlPostHashtagAPIListView(BaseAPIView):
    """해시태그 포스팅"""

    def get(self, request, user_id, format=None):
        # item_query = CrawlSearchTagRelatedPost.objects.filter(post__user__insta_pk=user_id, post__sidecar_parent__isnull=True)
        # sub_count_query = Count(Subquery(item_query.filter(searchtag=OuterRef('searchtag')).values('pk')))

        # items = item_query\
        # .annotate(
        #     count=Count('searchtag__name', distinct=True)
        # ).order_by('-count').values('searchtag__name', 'count', 'searchtag__media_count')

        items = CrawlSearchTag.objects.filter(posts__user__insta_pk=user_id, posts__sidecar_parent__isnull=True)\
            .annotate(count=Count('name'))\
            .order_by('-count').values('count','name', 'media_count')

        # print(items)
        paginator = LargeResultsSetPagination()
        result_page = paginator.paginate_queryset(items, request)
        # serializer = CrawlSearchTagRelatedPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(result_page)


class CrawlPostTopHashtagAPIListView(BaseAPIView):
    """해시태그 인기 포스팅"""

    def get(self, request, user_id, format=None):
        items = CrawlSearchTagRelatedPost.objects.filter(post__user__insta_pk=user_id, post__sidecar_parent__isnull=True, is_top=True).order_by('post').distinct('post').all()
        paginator = LargeResultsSetPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlSearchTagRelatedPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CrawlPostUserTagsAPIListView(BaseAPIView):
    """멘션 있는 포스팅"""

    def get(self, request, user_id, format=None):
        items = CrawlPostUserTags.objects.filter(post__user__insta_pk=user_id, post__sidecar_parent__isnull=True).order_by('post').distinct('post').all()
        paginator = LargeResultsSetPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlPostUserTagsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# class CrawlPostCaptionAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostCaption.objects.get(pk=id)
#             serializer = CrawlPostCaptionSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostCaption.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostCaption.objects.get(pk=id)
#         except CrawlPostCaption.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostCaptionSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostCaption.objects.get(pk=id)
#         except CrawlPostCaption.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostCaptionAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostCaption.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostCaptionSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostCaptionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostLikerAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostLiker.objects.get(pk=id)
#             serializer = CrawlPostLikerSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostLiker.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostLiker.objects.get(pk=id)
#         except CrawlPostLiker.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostLikerSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostLiker.objects.get(pk=id)
#         except CrawlPostLiker.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostLikerAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostLiker.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostLikerSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostLikerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlUserSimilarAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlUserSimilar.objects.get(pk=id)
#             serializer = CrawlUserSimilarSerializer(item)
#             return Response(serializer.data)
#         except CrawlUserSimilar.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlUserSimilar.objects.get(pk=id)
#         except CrawlUserSimilar.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlUserSimilarSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlUserSimilar.objects.get(pk=id)
#         except CrawlUserSimilar.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


class CrawlUserSimilarAPIListView(BaseAPIView):
    """비슷한 계정"""
    def get(self, request, user_id, format=None):
        items = CrawlUserSimilar.objects.filter(target_user__insta_pk=user_id)
        # items = CrawlUserSimilar.objects.order_by('pk')
        paginator = LargeResultsSetPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlUserSimilarSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlUserSimilarSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlUserFollowerAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlUserFollower.objects.get(pk=id)
#             serializer = CrawlUserFollowerSerializer(item)
#             return Response(serializer.data)
#         except CrawlUserFollower.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlUserFollower.objects.get(pk=id)
#         except CrawlUserFollower.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlUserFollowerSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlUserFollower.objects.get(pk=id)
#         except CrawlUserFollower.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


class CrawlUserFollowerAPIListView(BaseAPIView):

    def get(self, request, user_id, format=None):
        # items = CrawlUserFollower.objects.order_by('pk')
        items = CrawlUserFollower.objects.filter(target_user__insta_pk=user_id)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlUserFollowerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlUserFollowerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostLikerProxyAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostLikerProxy.objects.get(pk=id)
#             serializer = CrawlPostLikerProxySerializer(item)
#             return Response(serializer.data)
#         except CrawlPostLikerProxy.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostLikerProxy.objects.get(pk=id)
#         except CrawlPostLikerProxy.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostLikerProxySerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostLikerProxy.objects.get(pk=id)
#         except CrawlPostLikerProxy.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostLikerProxyAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostLikerProxy.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostLikerProxySerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostLikerProxySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlUserProfileProxyAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlUserProfileProxy.objects.get(pk=id)
#             serializer = CrawlUserProfileProxySerializer(item)
#             return Response(serializer.data)
#         except CrawlUserProfileProxy.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlUserProfileProxy.objects.get(pk=id)
#         except CrawlUserProfileProxy.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlUserProfileProxySerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlUserProfileProxy.objects.get(pk=id)
#         except CrawlUserProfileProxy.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlUserProfileProxyAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlUserProfileProxy.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlUserProfileProxySerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlUserProfileProxySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlUserFollowerProxyAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlUserFollowerProxy.objects.get(pk=id)
#             serializer = CrawlUserFollowerProxySerializer(item)
#             return Response(serializer.data)
#         except CrawlUserFollowerProxy.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlUserFollowerProxy.objects.get(pk=id)
#         except CrawlUserFollowerProxy.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlUserFollowerProxySerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlUserFollowerProxy.objects.get(pk=id)
#         except CrawlUserFollowerProxy.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlUserFollowerProxyAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlUserFollowerProxy.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlUserFollowerProxySerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlUserFollowerProxySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlCarouselMediaAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlCarouselMedia.objects.get(pk=id)
#             serializer = CrawlCarouselMediaSerializer(item)
#             return Response(serializer.data)
#         except CrawlCarouselMedia.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlCarouselMedia.objects.get(pk=id)
#         except CrawlCarouselMedia.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlCarouselMediaSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlCarouselMedia.objects.get(pk=id)
#         except CrawlCarouselMedia.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlCarouselMediaAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlCarouselMedia.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlCarouselMediaSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlCarouselMediaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostImageVersion2CandidateAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostImageVersion2Candidate.objects.get(pk=id)
#             serializer = CrawlPostImageVersion2CandidateSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostImageVersion2Candidate.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostImageVersion2Candidate.objects.get(pk=id)
#         except CrawlPostImageVersion2Candidate.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostImageVersion2CandidateSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostImageVersion2Candidate.objects.get(pk=id)
#         except CrawlPostImageVersion2Candidate.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostImageVersion2CandidateAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostImageVersion2Candidate.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostImageVersion2CandidateSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostImageVersion2CandidateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostVideoVersionAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostVideoVersion.objects.get(pk=id)
#             serializer = CrawlPostVideoVersionSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostVideoVersion.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostVideoVersion.objects.get(pk=id)
#         except CrawlPostVideoVersion.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostVideoVersionSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostVideoVersion.objects.get(pk=id)
#         except CrawlPostVideoVersion.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostVideoVersionAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostVideoVersion.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostVideoVersionSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostVideoVersionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostCommentAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostComment.objects.get(pk=id)
#             serializer = CrawlPostCommentSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostComment.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostComment.objects.get(pk=id)
#         except CrawlPostComment.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostCommentSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostComment.objects.get(pk=id)
#         except CrawlPostComment.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


class CrawlPostCommentAPIListView(BaseAPIView):

    def get(self, request, user_id=None, code=None, post_id=None, format=None):
        items = []
        if user_id != None:
            items = CrawlPostComment.objects.filter(post__user__insta_pk=user_id).order_by('-insta_pk').distinct('insta_pk')
        elif code != None:
            items = CrawlPostComment.objects.filter(post__code=code).order_by('-insta_pk').distinct('insta_pk')
        elif post_id != None:
            items = CrawlPostComment.objects.filter(post__insta_pk=post_id).order_by('-insta_pk').distinct('insta_pk')

            
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlPostCommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostCommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostLocationAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostLocation.objects.get(pk=id)
#             serializer = CrawlPostLocationSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostLocation.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostLocation.objects.get(pk=id)
#         except CrawlPostLocation.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostLocationSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostLocation.objects.get(pk=id)
#         except CrawlPostLocation.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostLocationAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostLocation.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostLocationSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostLocationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlPostUserTagsAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlPostUserTags.objects.get(pk=id)
#             serializer = CrawlPostUserTagsSerializer(item)
#             return Response(serializer.data)
#         except CrawlPostUserTags.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlPostUserTags.objects.get(pk=id)
#         except CrawlPostUserTags.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlPostUserTagsSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlPostUserTags.objects.get(pk=id)
#         except CrawlPostUserTags.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlPostUserTagsAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlPostUserTags.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlPostUserTagsSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlPostUserTagsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlSearchTagRelatedPostAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagRelatedPost.objects.get(pk=id)
#             serializer = CrawlSearchTagRelatedPostSerializer(item)
#             return Response(serializer.data)
#         except CrawlSearchTagRelatedPost.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagRelatedPost.objects.get(pk=id)
#         except CrawlSearchTagRelatedPost.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlSearchTagRelatedPostSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagRelatedPost.objects.get(pk=id)
#         except CrawlSearchTagRelatedPost.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


class CrawlSearchTagRelatedPostAPIListView(BaseAPIView):

    def get(self, request, tag, format=None):
        items = CrawlSearchTagRelatedPost.objects.filter(searchtag__name=tag).order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CrawlSearchTagRelatedPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlSearchTagRelatedPostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlRelatedTagAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlRelatedTag.objects.get(pk=id)
#             serializer = CrawlRelatedTagSerializer(item)
#             return Response(serializer.data)
#         except CrawlRelatedTag.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlRelatedTag.objects.get(pk=id)
#         except CrawlRelatedTag.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlRelatedTagSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlRelatedTag.objects.get(pk=id)
#         except CrawlRelatedTag.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlRelatedTagAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlRelatedTag.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlRelatedTagSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlRelatedTagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlSearchTagAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlSearchTag.objects.get(pk=id)
#             serializer = CrawlSearchTagSerializer(item)
#             return Response(serializer.data)
#         except CrawlSearchTag.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlSearchTag.objects.get(pk=id)
#         except CrawlSearchTag.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlSearchTagSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlSearchTag.objects.get(pk=id)
#         except CrawlSearchTag.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlSearchTagAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlSearchTag.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlSearchTagSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlSearchTagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlSearchTagSnapshotAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagSnapshot.objects.get(pk=id)
#             serializer = CrawlSearchTagSnapshotSerializer(item)
#             return Response(serializer.data)
#         except CrawlSearchTagSnapshot.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagSnapshot.objects.get(pk=id)
#         except CrawlSearchTagSnapshot.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlSearchTagSnapshotSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagSnapshot.objects.get(pk=id)
#         except CrawlSearchTagSnapshot.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlSearchTagSnapshotAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlSearchTagSnapshot.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlSearchTagSnapshotSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlSearchTagSnapshotSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlSearchTagProxyAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagProxy.objects.get(pk=id)
#             serializer = CrawlSearchTagProxySerializer(item)
#             return Response(serializer.data)
#         except CrawlSearchTagProxy.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagProxy.objects.get(pk=id)
#         except CrawlSearchTagProxy.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlSearchTagProxySerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlSearchTagProxy.objects.get(pk=id)
#         except CrawlSearchTagProxy.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlSearchTagProxyAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlSearchTagProxy.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlSearchTagProxySerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlSearchTagProxySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlLocationRelatedPostAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlLocationRelatedPost.objects.get(pk=id)
#             serializer = CrawlLocationRelatedPostSerializer(item)
#             return Response(serializer.data)
#         except CrawlLocationRelatedPost.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlLocationRelatedPost.objects.get(pk=id)
#         except CrawlLocationRelatedPost.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlLocationRelatedPostSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlLocationRelatedPost.objects.get(pk=id)
#         except CrawlLocationRelatedPost.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlLocationRelatedPostAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlLocationRelatedPost.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlLocationRelatedPostSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlLocationRelatedPostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlLocationFeedAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlLocationFeed.objects.get(pk=id)
#             serializer = CrawlLocationFeedSerializer(item)
#             return Response(serializer.data)
#         except CrawlLocationFeed.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlLocationFeed.objects.get(pk=id)
#         except CrawlLocationFeed.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlLocationFeedSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlLocationFeed.objects.get(pk=id)
#         except CrawlLocationFeed.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlLocationFeedAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlLocationFeed.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlLocationFeedSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlLocationFeedSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CrawlLocationFeedSnapshotAPIView(BaseAPIView):

#     def get(self, request, id, format=None):
#         try:
#             item = CrawlLocationFeedSnapshot.objects.get(pk=id)
#             serializer = CrawlLocationFeedSnapshotSerializer(item)
#             return Response(serializer.data)
#         except CrawlLocationFeedSnapshot.DoesNotExist:
#             return Response(status=404)

#     def put(self, request, id, format=None):
#         try:
#             item = CrawlLocationFeedSnapshot.objects.get(pk=id)
#         except CrawlLocationFeedSnapshot.DoesNotExist:
#             return Response(status=404)
#         serializer = CrawlLocationFeedSnapshotSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     def delete(self, request, id, format=None):
#         try:
#             item = CrawlLocationFeedSnapshot.objects.get(pk=id)
#         except CrawlLocationFeedSnapshot.DoesNotExist:
#             return Response(status=404)
#         item.delete()
#         return Response(status=204)


# class CrawlLocationFeedSnapshotAPIListView(BaseAPIView):

#     def get(self, request, format=None):
#         items = CrawlLocationFeedSnapshot.objects.order_by('pk')
#         paginator = PageNumberPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = CrawlLocationFeedSnapshotSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CrawlLocationFeedSnapshotSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
