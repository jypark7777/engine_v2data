from rest_framework.routers import SimpleRouter
from django.conf.urls import include, url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from instagram_crawler.views.data import ajax_save_crawler
from instagram_crawler.views import api
from django.urls import path

schema_view = get_schema_view(
   openapi.Info(
      title="Instagram API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@featuring.in"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

  path('ajax_save_crawler/', ajax_save_crawler, name='ajax_save_crawler'),

  

#   url(r'^crawlrecord/(?P<id>[0-9]+)/$', api.CrawlRecordAPIView.as_view()),
#   url(r'^crawlrecord/$', api.CrawlRecordAPIListView.as_view()),

#   url(r'^crawlprofileimage/(?P<id>[0-9]+)/$', api.CrawlProfileImageAPIView.as_view()),
#   url(r'^crawlprofileimage/$', api.CrawlProfileImageAPIListView.as_view()),

  url(r'^crawluserprofilesnapshot/(?P<user_id>[0-9]+)/$', api.CrawlUserProfileSnapshotAPIView.as_view()),
  url(r'^crawluserprofilesnapshot/(?P<user_id>[0-9]+)/list/', api.CrawlUserProfileSnapshotAPIListView.as_view()),

  url(r'^crawluserprofile/(?P<user_id>[0-9]+)/$', api.CrawlUserProfileAPIView.as_view()),
   path('crawluserprofile/u/<username>/', api.CrawlUserProfileUsernameAPIView.as_view()),

#   url(r'^crawluserprofile/$', api.CrawlUserProfileAPIListView.as_view()),

#   url(r'^crawlpostsnapshot/(?P<id>[0-9]+)/$', api.CrawlPostSnapshotAPIView.as_view()),
#   url(r'^crawlpostsnapshot/$', api.CrawlPostSnapshotAPIListView.as_view()),

  path('crawlpost/<code>/', api.CrawlPostAPIView.as_view()),

  url(r'^crawlpost/(?P<post_id>[0-9]+)/comment/list/$', api.CrawlPostCommentAPIListView.as_view()),
  path('crawlpost/c/<code>/comment/list/', api.CrawlPostCommentAPIListView.as_view()),

  url(r'^crawlpost/(?P<user_id>[0-9]+)/list/$', api.CrawlPostAPIListView.as_view()),
  url(r'^crawlpost/(?P<user_id>[0-9]+)/list/tophashtag', api.CrawlPostTopHashtagAPIListView.as_view()),
  url(r'^crawlpost/(?P<user_id>[0-9]+)/list/usertags', api.CrawlPostUserTagsAPIListView.as_view()),
  url(r'^crawlpost/(?P<user_id>[0-9]+)/list/hashtag', api.CrawlPostHashtagAPIListView.as_view()),

#   url(r'^crawlpostcaption/(?P<id>[0-9]+)/$', api.CrawlPostCaptionAPIView.as_view()),
#   url(r'^crawlpostcaption/$', api.CrawlPostCaptionAPIListView.as_view()),

#   url(r'^crawlpostliker/(?P<id>[0-9]+)/$', api.CrawlPostLikerAPIView.as_view()),
#   url(r'^crawlpostliker/$', api.CrawlPostLikerAPIListView.as_view()),

#   url(r'^crawlusersimilar/(?P<id>[0-9]+)/$', api.CrawlUserSimilarAPIView.as_view()),
  url(r'^crawlusersimilar/(?P<user_id>[0-9]+)/list$', api.CrawlUserSimilarAPIListView.as_view()),

#   url(r'^crawluserfollower/(?P<id>[0-9]+)/$', api.CrawlUserFollowerAPIView.as_view()),
#   url(r'^crawluserfollower/$', api.CrawlUserFollowerAPIListView.as_view()),
  url(r'^crawluserfollower/(?P<user_id>[0-9]+)/list/$', api.CrawlUserFollowerAPIListView.as_view()),

#   url(r'^crawlpostlikerproxy/(?P<id>[0-9]+)/$', api.CrawlPostLikerProxyAPIView.as_view()),
#   url(r'^crawlpostlikerproxy/$', api.CrawlPostLikerProxyAPIListView.as_view()),

#   url(r'^crawluserprofileproxy/(?P<id>[0-9]+)/$', api.CrawlUserProfileProxyAPIView.as_view()),
#   url(r'^crawluserprofileproxy/$', api.CrawlUserProfileProxyAPIListView.as_view()),

#   url(r'^crawluserfollowerproxy/(?P<id>[0-9]+)/$', api.CrawlUserFollowerProxyAPIView.as_view()),
#   url(r'^crawluserfollowerproxy/$', api.CrawlUserFollowerProxyAPIListView.as_view()),

#   url(r'^crawlcarouselmedia/(?P<id>[0-9]+)/$', api.CrawlCarouselMediaAPIView.as_view()),
#   url(r'^crawlcarouselmedia/$', api.CrawlCarouselMediaAPIListView.as_view()),

#   url(r'^crawlpostimageversion2candidate/(?P<id>[0-9]+)/$', api.CrawlPostImageVersion2CandidateAPIView.as_view()),
#   url(r'^crawlpostimageversion2candidate/$', api.CrawlPostImageVersion2CandidateAPIListView.as_view()),

#   url(r'^crawlpostvideoversion/(?P<id>[0-9]+)/$', api.CrawlPostVideoVersionAPIView.as_view()),
#   url(r'^crawlpostvideoversion/$', api.CrawlPostVideoVersionAPIListView.as_view()),

#   url(r'^crawlpostcomment/(?P<id>[0-9]+)/$', api.CrawlPostCommentAPIView.as_view()),
  url(r'^crawlpostcomment/(?P<user_id>[0-9]+)/list/$', api.CrawlPostCommentAPIListView.as_view()),

#   url(r'^crawlpostlocation/(?P<id>[0-9]+)/$', api.CrawlPostLocationAPIView.as_view()),
#   url(r'^crawlpostlocation/$', api.CrawlPostLocationAPIListView.as_view()),

#   url(r'^crawlpostusertags/(?P<id>[0-9]+)/$', api.CrawlPostUserTagsAPIView.as_view()),
#   url(r'^crawlpostusertags/$', api.CrawlPostUserTagsAPIListView.as_view()),

#   url(r'^crawlsearchtagrelatedpost/(?P<id>[0-9]+)/$', api.CrawlSearchTagRelatedPostAPIView.as_view()),
#   url(r'^crawlsearchtagrelatedpost/$', api.CrawlSearchTagRelatedPostAPIListView.as_view()),

#   path('crawlsearchtagrelatedpost/tag/<tag>/list/', api.CrawlSearchTagRelatedPostAPIListView.as_view()), #해시태그 포스팅
  path('crawlsearchtagrelatedpost/tag/<tag>/list/user/', api.CrawlSearchTagRelatedPostAPIListView.as_view()), #해시태그 포스팅 유저 
  path('crawlsearchtagrelatedpost/tag/<tag>/list/top/user/', api.CrawlSearchTagRelatedPostAPIListView.as_view()), #해시태그 인기포스팅 유저


#   url(r'^crawlrelatedtag/(?P<id>[0-9]+)/$', api.CrawlRelatedTagAPIView.as_view()),
#   url(r'^crawlrelatedtag/$', api.CrawlRelatedTagAPIListView.as_view()),
  
#   url(r'^crawlsearchtag/(?P<id>[0-9]+)/$', api.CrawlSearchTagAPIView.as_view()),
#   url(r'^crawlsearchtag/$', api.CrawlSearchTagAPIListView.as_view()),

#   url(r'^crawlsearchtagsnapshot/(?P<id>[0-9]+)/$', api.CrawlSearchTagSnapshotAPIView.as_view()),
#   url(r'^crawlsearchtagsnapshot/$', api.CrawlSearchTagSnapshotAPIListView.as_view()),

#   url(r'^crawlsearchtagproxy/(?P<id>[0-9]+)/$', api.CrawlSearchTagProxyAPIView.as_view()),
#   url(r'^crawlsearchtagproxy/$', api.CrawlSearchTagProxyAPIListView.as_view()),

#   url(r'^crawllocationrelatedpost/(?P<id>[0-9]+)/$', api.CrawlLocationRelatedPostAPIView.as_view()),
#   url(r'^crawllocationrelatedpost/$', api.CrawlLocationRelatedPostAPIListView.as_view()),

#   url(r'^crawllocationfeed/(?P<id>[0-9]+)/$', api.CrawlLocationFeedAPIView.as_view()),
#   url(r'^crawllocationfeed/$', api.CrawlLocationFeedAPIListView.as_view()),

#   url(r'^crawllocationfeedsnapshot/(?P<id>[0-9]+)/$', api.CrawlLocationFeedSnapshotAPIView.as_view()),
#   url(r'^crawllocationfeedsnapshot/$', api.CrawlLocationFeedSnapshotAPIListView.as_view()),
]

