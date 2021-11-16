from datetime import datetime, timezone, timedelta
from .models import *
from django.db.models import Q

import time
from django.db import transaction
from django.forms import model_to_dict
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError
import traceback
from django.db.models import Subquery


class InstagramCrawlerDataSet:
    current_now = None
    crawlerRecord = None

    def __init__(self, crawlerRecord=None):
        self.current_now = datetime.now(timezone.utc)

        if crawlerRecord == None:
            self.crawlerRecord = CrawlRecord()
            self.crawlerRecord.from_source = 1
            self.crawlerRecord.save()
        else:
            self.crawlerRecord = crawlerRecord

    def saveCrawlFollowerBulk(self, targetCrawlUser, followers_json_list):
        create_users_models = []
        create_followers_models = []

        append_pk = {}
        for follower_item in followers_json_list:
            if follower_item['pk'] not in append_pk:
                if CrawlUserProfile.objects.filter(insta_pk=follower_item['pk']).exists() == False:
                    crawlUser = CrawlUserProfile()
                    crawlUser.jsonToClass(follower_item)
                    create_users_models.append(crawlUser)
                    append_pk[follower_item['pk']] = True

        try:
            create = CrawlUserProfile.objects.bulk_create(create_users_models)
        except:
            for userProfileItem in create_users_models:
                try:
                    userProfileItem.save()
                except:
                    pass


        append_pk = {}
        for follower_item in followers_json_list:
            if follower_item['pk'] not in append_pk:
                try:
                    crawlUser = CrawlUserProfile.objects.get(insta_pk=follower_item['pk'])
                    if targetCrawlUser.follower.count() == 0 or (targetCrawlUser.follower.count() > 0 and CrawlUserFollower.objects.filter(target_user=targetCrawlUser, user=crawlUser).exists() == False):
                        crawlProfileFollower = CrawlUserFollower()
                        crawlProfileFollower.record = self.crawlerRecord
                        crawlProfileFollower.target_user = targetCrawlUser
                        crawlProfileFollower.user = crawlUser
                        create_followers_models.append(crawlProfileFollower)
                        append_pk[follower_item['pk']] = True
                except:
                    pass

        # print('bulk : ', len(create_users_models), len(create_followers_models))
        try:
            f_create = CrawlUserFollower.objects.bulk_create(create_followers_models)
        except:
            for followerItem in create_followers_models:
                try:
                    followerItem.save()
                except:
                    pass

        # print('result : ', create, f_create)

    def saveCrawlFollower(self, targetCrawlUser, response_follower_json):
        crawlProfileFollower = None
        user = self.saveCrawlUser(response_follower_json)

        try:
            crawlProfileFollower = CrawlUserFollower.objects.get(target_user=targetCrawlUser, user=user)
        except CrawlUserFollower.DoesNotExist:
            crawlProfileFollower = CrawlUserFollower()

        crawlProfileFollower.record = self.crawlerRecord
        crawlProfileFollower.target_user = targetCrawlUser
        crawlProfileFollower.user = user

        try:
            crawlProfileFollower.save()
        except IntegrityError:
            pass

        return crawlProfileFollower

    @transaction.atomic
    def saveCrawlFollowing(self, targetCrawlUser, response_following_json):
        crawlProfileFollowing = None
        user = self.saveCrawlUser(response_following_json)
        try:
            crawlProfileFollowing = CrawlUserFollower.objects.get(target_user=user, user=targetCrawlUser)
        except CrawlUserFollower.DoesNotExist:
            crawlProfileFollowing = CrawlUserFollower()

        crawlProfileFollowing.record = self.crawlerRecord
        crawlProfileFollowing.target_user = user
        crawlProfileFollowing.user = targetCrawlUser

        try:
            crawlProfileFollowing.save()
        except IntegrityError:
            pass

        return crawlProfileFollowing


    def saveCrawlPostLikerBulk(self, crawlPost, postliker_json_list):
        create_users_models = []
        create_likers_models = []

        append_pk = {}
        for liker_item in postliker_json_list:
            if liker_item['pk'] not in append_pk:
                if CrawlUserProfile.objects.filter(insta_pk=liker_item['pk']).exists() == False:
                    crawlUser = CrawlUserProfile()
                    crawlUser.jsonToClass(liker_item)
                    create_users_models.append(crawlUser)
                    append_pk[liker_item['pk']] = True

        try:
            create = CrawlUserProfile.objects.bulk_create(create_users_models)
        except:
            for userProfileItem in create_users_models:
                try:
                    userProfileItem.save()
                except:
                    pass


        append_pk = {}
        for liker_item in postliker_json_list:
            if liker_item['pk'] not in append_pk:
                crawlUser = CrawlUserProfile.objects.get(insta_pk=liker_item['pk'])
                if crawlPost.liker.count() == 0 or (crawlPost.liker.count() > 0 and CrawlPostLiker.objects.filter(post=crawlPost, user=crawlUser).exists() == False):
                    crawlPostLiker = CrawlPostLiker()
                    crawlPostLiker.record = self.crawlerRecord
                    crawlPostLiker.post = crawlPost
                    crawlPostLiker.user = crawlUser
                    create_likers_models.append(crawlPostLiker)
                    append_pk[liker_item['pk']] = True

        # print('bulk : ', len(create_users_models), len(create_followers_models))
        try:
            f_create = CrawlPostLiker.objects.bulk_create(create_likers_models)
        except:
            for saveItem in create_likers_models:
                try:
                    saveItem.save()
                except:
                    pass

        # print('result : ', create, f_create)


    @transaction.atomic
    def saveCrawlPostLiker(self, crawlPost, response_postliker_json):
        crawlPostLiker = None
        user = self.saveCrawlUser(response_postliker_json)
        try:
            crawlPostLiker = CrawlPostLiker.objects.get(post=crawlPost, user=user)
        except CrawlPostLiker.DoesNotExist:
            crawlPostLiker = CrawlPostLiker()

        crawlPostLiker.record = self.crawlerRecord
        crawlPostLiker.post = crawlPost
        crawlPostLiker.user = user

        try:
            crawlPostLiker.save()
        except IntegrityError:
            pass

        return crawlPostLiker



    def saveCrawlPostComment(self,crawlPost, response_postcomment_json, targetCrawlUser=None):
        crawlPostComment = None
        try:
            if 'pk' in response_postcomment_json:
                pk = response_postcomment_json['pk']
            elif 'insta_pk' in response_postcomment_json:
                pk = response_postcomment_json['insta_pk']
            else:
                return None

            crawlPostComment = CrawlPostComment.objects.get(insta_pk=pk)
        except CrawlPostComment.DoesNotExist:
            crawlPostComment = CrawlPostComment()

        crawlPostComment.post = crawlPost
        crawlPostComment.record = self.crawlerRecord
        crawlPostComment.jsonToClass(response_postcomment_json)
        crawlPostComment.user = self.saveCrawlUser(response_postcomment_json['user'])

        try: #댓글 해시태그 저장
            if crawlPostComment.text != None and crawlPost.user == crawlPostComment.user:
                caption_text = crawlPostComment.text
                hashtags = parse_hashtags(caption_text)
                for hashtag in hashtags:
                    tag, _ = CrawlSearchTag.objects.get_or_create(name = hashtag)
                    tag.posts.add(crawlPost)
        except:
            pass
        
        try:
            crawlPostComment.save()
            # print('saveCrawlPostComment Save : ', pk )

        except IntegrityError:
            pass

        return crawlPostComment

    def saveCrawlUserSimilar(self, targetCrawlUser, response_target_json):
        crawlUserSimilar = None

        user = self.saveCrawlUser(response_target_json)
        crawlUserSimilar, _ = CrawlUserSimilar.objects.get_or_create(target_user=targetCrawlUser, user=user)
        # try:
        #     crawlUserSimilar = CrawlUserSimilar.objects.get(target_user=targetCrawlUser, user=user)
        # except CrawlUserSimilar.DoesNotExist:
        #     crawlUserSimilar = CrawlUserSimilar()

        # crawlUserSimilar.record = self.crawlerRecord
        # crawlUserSimilar.target_user = targetCrawlUser
        # crawlUserSimilar.user = user

        # try:
        #     crawlUserSimilar.save()
        # except IntegrityError:
        #     pass


        return crawlUserSimilar

    # @transaction.atomic
    def saveCrawlPost(self, targetCrawlUser, response_post_json, sidecar_parent_post=None):
        crawlPost = None
        crawlPostCreated = False
        # print('saveCrawlPost - response_post_json : ' , response_post_json)

        try:
            if 'pk' in response_post_json:
                pk = response_post_json['pk']
            elif 'insta_pk' in response_post_json:
                pk = response_post_json['insta_pk']
            else:
                return None

            crawlPost = CrawlPost.objects.get(insta_pk=pk)
        except CrawlPost.DoesNotExist:
            crawlPost = CrawlPost()
            crawlPostCreated = True

        crawlPost.record = self.crawlerRecord

        crawlPost.user = targetCrawlUser
        crawlPost.jsonToClass(response_post_json)

        if sidecar_parent_post != None:
            crawlPost.sidecar_parent = sidecar_parent_post


        try:
            crawlPost.save()
        except:
            print('saveCrawlPost - crawlPost.save error : ' , traceback.format_exc())

        try:
            if crawlPostCreated == False:
                model_dict = model_to_dict(crawlPost, exclude=['id','record','user','snap_date', 'snap_time'])
                snapInstance = CrawlPostSnapshot()
                snapInstance.record = crawlPost.record
                snapInstance.user = crawlPost.user
                snapInstance.jsonToClass(response_post_json)
                snapInstance.save()
        except:
            print('saveCrawlPost - snapInstance.save() : ' , traceback.format_exc())

        if 'caption' in response_post_json and response_post_json['caption'] != None:
            caption_json = response_post_json['caption']
            try:
                crawlPostCaption, is_created = CrawlPostCaption.objects.get_or_create(post=crawlPost)
            except MultipleObjectsReturned:
                crawlPostCaption = CrawlPostCaption.objects.filter(post=crawlPost).last()

            crawlPostCaption.record = self.crawlerRecord
            crawlPostCaption.jsonToClass(caption_json)

            

            try:
                crawlPostCaption.save()
            except IntegrityError:
                pass
            
            try:
                if 'text' in caption_json and caption_json['text']:
                    caption_text = caption_json['text']
                    hashtags = parse_hashtags(caption_text)
                    for hashtag in hashtags:
                        tag, _ = CrawlSearchTag.objects.get_or_create(name = hashtag)
                        tag.posts.add(crawlPost)
            except:
                pass


            # try:
            #     kwargs = model_to_dict(crawlPostCaption, exclude=['id','record','post','snap_date', 'snap_time'])
            #     snapInstance = CrawlPostCaptionSnapshot()
            #     snapInstance.record = crawlPostCaption.record
            #     snapInstance.post = crawlPostCaption.post
            #     snapInstance.jsonToClass(caption_json)
            #     snapInstance.save()
            # except:
            #     pass

        try:
            if 'image_versions2' in response_post_json and response_post_json['image_versions2'] != None:
                image_versions2_json = response_post_json['image_versions2']
                candidates_json = image_versions2_json['candidates']
                for candidate_json in candidates_json:
                    if 'url' in candidate_json:
                        is_exists = CrawlPostImageVersion2Candidate.objects.filter(post = crawlPost, url=candidate_json['url'], width=candidate_json['width']).exists()
                        if is_exists == False:
                            crawlPostImageVersion2Candidate = CrawlPostImageVersion2Candidate()
                            crawlPostImageVersion2Candidate.record = self.crawlerRecord
                            crawlPostImageVersion2Candidate.post = crawlPost
                            crawlPostImageVersion2Candidate.jsonToClass(candidate_json)
                            crawlPostImageVersion2Candidate.save()

            elif 'video_versions' in response_post_json and response_post_json['video_versions'] != None:
                video_versions = response_post_json['video_versions']
                candidates_json = video_versions['candidates']
                for candidate_json in candidates_json:
                    if 'url' in candidate_json:
                        is_exists = CrawlPostVideoVersion.objects.filter(post = crawlPost, url=candidate_json['url'], width=candidate_json['width']).exists()
                        if is_exists == False:
                            crawlPostVideoVersion = CrawlPostVideoVersion()
                            crawlPostVideoVersion.record = self.crawlerRecord
                            crawlPostVideoVersion.post = crawlPost
                            crawlPostVideoVersion.jsonToClass(candidate_json)
                            crawlPostVideoVersion.save()

            elif 'carousel_media' in response_post_json and response_post_json['carousel_media'] != None:
                carousel_media_json = response_post_json['carousel_media']
                for media_json in carousel_media_json:
                    if 'pk' in media_json:
                        crawlCarouselMedia, is_created = CrawlCarouselMedia.objects.get_or_create(insta_pk=media_json['pk'])
                    else:
                        crawlCarouselMedia = CrawlCarouselMedia()

                    crawlCarouselMedia.record = self.crawlerRecord
                    crawlCarouselMedia.post = crawlPost
                    crawlCarouselMedia.jsonToClass(media_json)
                    crawlCarouselMedia.save()
                    # print('crawlCarouselMedia : ', crawlCarouselMedia.pk)

                    if 'image_versions2' in media_json and media_json['image_versions2'] != None:
                        image_versions2_json = media_json['image_versions2']
                        candidates_json = image_versions2_json['candidates']
                        for candidate_json in candidates_json:
                            crawlPostImageVersion2Candidate = CrawlPostImageVersion2Candidate()
                            crawlPostImageVersion2Candidate.post = crawlPost
                            crawlPostImageVersion2Candidate.record = self.crawlerRecord
                            crawlPostImageVersion2Candidate.carousel_media = crawlCarouselMedia
                            crawlPostImageVersion2Candidate.jsonToClass(candidate_json)
                            crawlPostImageVersion2Candidate.save()

                    elif 'video_versions' in media_json and media_json['video_versions'] != None:
                        video_versions_json = media_json['video_versions']
                        for video_version in video_versions_json:
                            crawlPostVideoVersion = CrawlPostVideoVersion()
                            crawlPostVideoVersion.post = crawlPost
                            crawlPostVideoVersion.record = self.crawlerRecord
                            crawlPostVideoVersion.carousel_media = crawlCarouselMedia
                            crawlPostVideoVersion.jsonToClass(video_version)
                            crawlPostVideoVersion.save()
        except:
            print('saveCrawlPost - image_versions2 : ' , traceback.format_exc())

        try:
            if 'sidecar_children' in response_post_json and response_post_json['sidecar_children'] != None:
                sidecars_json = response_post_json['sidecar_children']
                for sidecar_json in sidecars_json:
                    self.saveCrawlPost(targetCrawlUser,sidecar_json, sidecar_parent_post=crawlPost)

        except:
            print('saveCrawlPost - sidecar_children : ' , traceback.format_exc())

        try:
            if 'location' in response_post_json and response_post_json['location'] != None:
                location_json = response_post_json['location']
                if 'pk' in location_json:
                    # crawlPostLocation, is_create = CrawlPostLocation.objects.get_or_create(insta_pk=location_json['pk'])
                    crawlPostLocation = None
                    try:
                        crawlPostLocation = CrawlPostLocation.objects.get(insta_pk=location_json['pk'])
                    except:
                        crawlPostLocation = CrawlPostLocation(insta_pk=location_json['pk'])
                        crawlPostLocation.save()

                    crawlPostLocation.post.add(crawlPost)
                    crawlPostLocation.record = self.crawlerRecord
                    crawlPostLocation.jsonToClass(location_json)
                    crawlPostLocation.save()
                    # print('crawlPostLocation : ' , location_json['name'])
        except:
            print('crawlPostLocation error', traceback.format_exc())
            # pass

        try:
            if 'usertags' in response_post_json and response_post_json['usertags'] != None:
                usertags_json = response_post_json['usertags']
                if 'in' in usertags_json and usertags_json['in'] != None:
                    usertags_in_json = usertags_json['in']
                    for usertag_in in usertags_in_json:
                        user_json = usertag_in['user']
                        positions = usertag_in['position']
                        user = self.getCrawlUser(user_json['pk'])
                        if user == None:
                            user = self.saveCrawlUser(user_json)

                        crawlPostUserTags, is_created = CrawlPostUserTags.objects.get_or_create(post=crawlPost, user=user)
                        crawlPostUserTags.record = self.crawlerRecord

                        if len(positions) > 1:
                            # crawlPostUserTags.position_x = round(positions[0],6)
                            # crawlPostUserTags.position_y = round(positions[1],6)
                            crawlPostUserTags.position_x = positions[0]
                            crawlPostUserTags.position_y = positions[1]
                            # print(crawlPostUserTags.position_x , crawlPostUserTags.position_y)

                        # crawlPostUserTags.jsonToClass(usertag_in)
                        # print(crawlPostUserTags.post, crawlPostUserTags.reocrd, crawlPostUserTags.position_x, crawlPostUserTags.position_y, crawlPostUserTags.user)
                        crawlPostUserTags.save()
        except:
            # pass
            print('crawlPostUserTags error', traceback.format_exc())

        # print('saveCrawlPost - return : ' , crawlPost)
        try:
            crawlPost.save()
        except:
            print('saveCrawlPost - crawlPost.save error : ' , traceback.format_exc())

        return crawlPost

    @transaction.atomic
    def saveCrawlUser(self, response_user_json, is_profile_crawled=False, username=None):
        crawlUserProfile = None
        start_time = time.time()
        if 'pk' in response_user_json:
            insta_pk = response_user_json['pk']
        elif 'insta_pk' in response_user_json:
            insta_pk = response_user_json['insta_pk']
        else:
            return None

        if 'id' in response_user_json:
            response_user_json.pop('id',None)

        try:
            crawlUserProfile = CrawlUserProfile.objects.get(insta_pk=insta_pk)
        except MultipleObjectsReturned:
            crawlUserProfile = CrawlUserProfile.objects.filter(insta_pk=insta_pk).last()
            CrawlUserProfile.objects.filter(insta_pk=insta_pk).first().delete()
        except CrawlUserProfile.DoesNotExist:
            crawlUserProfile = CrawlUserProfile()

        # print('[saveCrawlUser] crawlUserProfile', (time.time()-start_time))

        crawlUserProfile.jsonToClass(response_user_json)
        # print('[saveCrawlUser] jsonToClass', (time.time()-start_time))

        crawlUserProfile.is_profile_crawled = is_profile_crawled
        if crawlUserProfile.following_count != None and crawlUserProfile.follower_count != None and crawlUserProfile.media_count != None or is_profile_crawled:
            crawlUserProfile.is_analy_requirements = True

        crawlUserProfile.record = self.crawlerRecord

        try:
            if username != None:
                crawlUserProfile.username = username

            # print('response_user_json : ', response_user_json)
            crawlUserProfile.save()
            # print('[saveCrawlUser] save', (time.time()-start_time))
        except IntegrityError:
            print('saveCrawlUser - crawlUserProfile.save() : ' , traceback.format_exc())

        try:
            if crawlUserProfile.is_analy_requirements or crawlUserProfile.is_profile_crawled:
                if 'follower_count' in response_user_json:
                    snapInstance = CrawlUserProfileSnapshot()
                    snapInstance.record = crawlUserProfile.record
                    snapInstance.jsonToClass(response_user_json)
                    snapInstance.save()

                    # print('[saveCrawlUser] snapInstance save', (time.time()-start_time))
        except:
            print('saveCrawlUser - snapInstance.save() : ' , traceback.format_exc())

        # print('[saveCrawlUser] complete', (time.time()-start_time))
        return crawlUserProfile


    def getCrawlUser(self, insta_pk):
        try:
            return CrawlUserProfile.objects.get(insta_pk=insta_pk)
        except MultipleObjectsReturned:
            crawlUserProfile = CrawlUserProfile.objects.filter(insta_pk=insta_pk).last()
            CrawlUserProfile.objects.filter(insta_pk=insta_pk).first().delete()
            return crawlUserProfile
        except CrawlUserProfile.DoesNotExist:
            return None

    def getCrawlNotProfileUsers(self, size=1000, shuffle=False):
        if shuffle:
            return CrawlUserProfile.objects.filter(is_profile_crawled=False, is_analy_requirements=False).order_by("?")[:size].all()

        return CrawlUserProfile.objects.filter(is_profile_crawled=False, is_analy_requirements=False)[:size].all()


    def getCrawlTrackingProfileUsers(self):
        pasttime = datetime.now() - timedelta(days=3)
        # RequestUserProfile.objects.filter(is_complete=True, is_suspend=False).all()
        return CrawlUserProfile.objects.filter(username__in=Subquery(RequestUserProfile.objects.filter(is_complete=True, is_suspend=False).values('username')), is_analy_requirements=True, updated_time__lte=pasttime).order_by('updated_time')[:50].all()


    @transaction.atomic
    def saveCrawlTag(self, response_tag_json, fromCrawlTag=None):
        crawlSearchTag = None

        if 'id' in response_tag_json:
            insta_id = response_tag_json['id']
        elif 'insta_id' in response_tag_json:
            insta_id = response_tag_json['insta_id']
        else:
            return None

        try:
            crawlSearchTag = CrawlSearchTag.objects.get(insta_id=insta_id)
        except MultipleObjectsReturned:
            crawlSearchTag = CrawlSearchTag.objects.filter(insta_id=insta_id).last()
            CrawlSearchTag.objects.filter(insta_id=insta_id).first().delete()
        except CrawlSearchTag.DoesNotExist:
            crawlSearchTag = CrawlSearchTag()

        crawlSearchTag.jsonToClass(response_tag_json)
        crawlSearchTag.record = self.crawlerRecord

        try:
            crawlSearchTag.save()
        except IntegrityError:
            pass

        if fromCrawlTag != None:
            crawlSearchTag.from_search_tag.add(fromCrawlTag)

        try:
            if 'media_count' in response_tag_json:
                snapInstance = CrawlSearchTagSnapshot()
                snapInstance.record = crawlSearchTag.record
                snapInstance.jsonToClass(response_tag_json)
                snapInstance.save()

        except:
            print('saveCrawlTag - snapInstance.save() : ' , traceback.format_exc())

        return crawlSearchTag




    @transaction.atomic
    def saveCrawlLocationFeed(self, response_location_json):
        crawlLocationFeed = None
        crawlPostLocation = None

        if 'id' in response_location_json:
            insta_id = response_location_json['id']
        elif 'insta_id' in response_location_json:
            insta_id = response_location_json['insta_id']
        else:
            return None

        try:
            crawlLocationFeed = CrawlLocationFeed.objects.get(insta_id=insta_id)
        except MultipleObjectsReturned:
            crawlLocationFeed = CrawlLocationFeed.objects.filter(insta_id=insta_id).last()
            CrawlLocationFeed.objects.filter(insta_id=insta_id).first().delete()
        except CrawlLocationFeed.DoesNotExist:
            crawlLocationFeed = CrawlLocationFeed()

        crawlLocationFeed.jsonToClass(response_location_json)
        crawlLocationFeed.record = self.crawlerRecord


        try:
            crawlPostLocation = CrawlPostLocation.objects.get(insta_pk=insta_id)
        except MultipleObjectsReturned:
            crawlPostLocation = CrawlPostLocation.objects.filter(insta_pk=insta_id).last()
            CrawlPostLocation.objects.filter(insta_pk=insta_id).first().delete()
        except:
            crawlPostLocation = CrawlPostLocation(insta_pk=insta_id)
            crawlPostLocation.save()

        crawlLocationFeed.location = crawlPostLocation


        try:
            crawlLocationFeed.save()
        except IntegrityError:
            pass

        try:
            if 'media_count' in response_location_json:
                snapInstance = CrawlLocationFeedSnapshot()
                snapInstance.record = crawlLocationFeed.record
                snapInstance.jsonToClass(response_location_json)
                snapInstance.save()

        except:
            print('saveCrawlTag - snapInstance.save() : ' , traceback.format_exc())

        return crawlLocationFeed

import re
def parse_hashtags(sentence, endswith=None):
    hash_pattern = '#([\w]*)'
    if endswith != None:
        hash_pattern = '#([\w]*%s)' % endswith
    hash_w = re.compile(hash_pattern)
    hash_tag = hash_w.findall(sentence)
    return hash_tag