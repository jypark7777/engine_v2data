from instagram_crawler.lambda_request.lambda_function import InstagramInfoScraper
from instagram_crawler.models import *
from instagram_crawler.instagram_crawler_dataset import InstagramCrawlerDataSet
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Subquery
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json


def saveExploreTag(tagname, result_tag_json, crawlRecord=None):
    crawlSearchTag = None
    try:

        if 'is_not_found' in result_tag_json:
            return None

        if result_tag_json != None:
            if crawlRecord == None:
                crawlRecord = CrawlRecord()
                crawlRecord.from_source = 2
                crawlRecord.save()

            dataSet = InstagramCrawlerDataSet(crawlRecord)
            crawlSearchTag = dataSet.saveCrawlTag(result_tag_json)

            if 'related_tags' in result_tag_json:
                if len(result_tag_json['related_tags']) > 0:
                    for tagitem in result_tag_json['related_tags']:
                        if 'node' in tagitem:
                            node = tagitem['node']
                            if 'name' in node:
                                tagitem_name = node['name']
                                relatedTag = None
                                try:
                                    relatedTag = CrawlRelatedTag.objects.get(name=tagitem_name)
                                except:
                                    relatedTag = CrawlRelatedTag(name=tagitem_name)
                                    relatedTag.save()

                                crawlSearchTag.related_tag.add(relatedTag)
            if 'posts' in result_tag_json:
                if len(result_tag_json['posts']) > 0:
                    for postitem in result_tag_json['posts']:
                        userProfile = dataSet.saveCrawlUser({'insta_pk' : postitem['user_insta_pk']})
                        return_post = dataSet.saveCrawlPost(userProfile, postitem)
                        if return_post != None:
                            try:
                                CrawlSearchTagRelatedPost.objects.create(searchtag=crawlSearchTag, post=return_post, is_top=False, record_id=dataSet.crawlerRecord.pk)
                            except:
                                continue
                    # saveTagPost.delay(dataSet.crawlerRecord.pk, crawlSearchTag.pk, postitem)

            if 'top' in result_tag_json:
                if len(result_tag_json['top']) > 0:
                    for postitem in result_tag_json['top']:
                        userProfile = dataSet.saveCrawlUser({'insta_pk' : postitem['user_insta_pk']})
                        return_post = dataSet.saveCrawlPost(userProfile, postitem)
                        if return_post != None:
                            try:
                                CrawlSearchTagRelatedPost.objects.create(searchtag=crawlSearchTag, post=return_post, is_top=True, record_id=dataSet.crawlerRecord.pk)
                            except:
                                continue
                    # print('top return_post : ', return_post, return_post.like_count)
                    # saveTagPost.delay(dataSet.crawlerRecord.pk, crawlSearchTag.pk, postitem, is_top=True)


    except:
        print('traceback : ', traceback.format_exc())

    if crawlSearchTag == None:
        try:
            crawlSearchTag = CrawlSearchTag.objects.get(name=tagname)
        except:
            print('traceback : ', traceback.format_exc())

    return crawlSearchTag



def saveLocation(location_id, result_location_json, crawlRecord=None):
    crawlLocationFeed = None
    try:

        if 'is_not_found' in result_location_json:
            return None

        if result_location_json != None:
            if crawlRecord == None:
                crawlRecord = CrawlRecord()
                crawlRecord.from_source = 2
                crawlRecord.save()

            dataSet = InstagramCrawlerDataSet(crawlRecord)
            crawlLocationFeed = dataSet.saveCrawlLocationFeed(result_location_json)

            if 'posts' in result_location_json:
                if len(result_location_json['posts']) > 0:
                    for postitem in result_location_json['posts']:
                        userProfile = dataSet.saveCrawlUser({'insta_pk' : postitem['user_insta_pk']})
                        return_post = dataSet.saveCrawlPost(userProfile, postitem)
                        if return_post != None:
                            try:
                                CrawlLocationRelatedPost.objects.create(location=crawlLocationFeed, post=return_post, is_top=False, record_id=dataSet.crawlerRecord.pk)
                                crawlLocationFeed.location.post.add(return_post)
                            except:
                                continue
                    # saveTagPost.delay(dataSet.crawlerRecord.pk, crawlSearchTag.pk, postitem)

            if 'top' in result_location_json:
                if len(result_location_json['top']) > 0:
                    for postitem in result_location_json['top']:
                        userProfile = dataSet.saveCrawlUser({'insta_pk' : postitem['user_insta_pk']})
                        return_post = dataSet.saveCrawlPost(userProfile, postitem)
                        if return_post != None:
                            try:
                                CrawlLocationRelatedPost.objects.create(location=crawlLocationFeed, post=return_post, is_top=True, record_id=dataSet.crawlerRecord.pk)
                                crawlLocationFeed.location.post.add(return_post)
                            except:
                                continue


    except:
        print('traceback : ', traceback.format_exc())

    if crawlLocationFeed == None:
        try:
            crawlLocationFeed = CrawlLocationFeed.objects.get(insta_id=location_id)
        except:
            print('traceback : ', traceback.format_exc())

    return crawlLocationFeed





def saveFindTag(tagname, result_tag_json, crawlRecord=None):
    crawlSearchTag = None
    try:
        if 'is_not_found' in result_tag_json:
            return None

        if len(result_tag_json) > 0:

            if crawlRecord == None:
                crawlRecord = CrawlRecord()
                crawlRecord.from_source = 2
                crawlRecord.save()
            dataSet = InstagramCrawlerDataSet(crawlRecord)

            fromTag_id = None
            for item in result_tag_json:
                if 'name' in item:
                    name = item['name']
                    if name == tagname:
                        crawlSearchTag = dataSet.saveCrawlTag(item)
                        fromTag_id = crawlSearchTag.pk
                    else:
                        # saveTag.delay(dataSet.crawlerRecord.pk, fromTag_id, item)
                        dataSet.saveCrawlTag(item, fromTag_id)


    except:
        print('traceback : ', traceback.format_exc())

    if crawlSearchTag == None:
        try:
            crawlSearchTag = CrawlSearchTag.objects.get(name=tagname)
        except:
            print('traceback : ', traceback.format_exc())

    return crawlSearchTag


def saveCrawlUser(username, result_user_json, crawlRecord=None):
    crawlUserProfile = None
    try:
        if 'is_not_found' in result_user_json:
            return None

        if crawlRecord == None:
            crawlRecord = CrawlRecord()
            crawlRecord.from_source = 2
            crawlRecord.save()

        dataSet = InstagramCrawlerDataSet(crawlRecord)
        result_user_json['username'] = username

        crawlUserProfile = dataSet.saveCrawlUser(result_user_json)
        if 'posts' in result_user_json:
            for post in result_user_json['posts']:
                return_post = dataSet.saveCrawlPost(crawlUserProfile, post)

        if 'similars' in result_user_json:
            for similar_user in result_user_json['similars']:
                return_similar = dataSet.saveCrawlUserSimilar(crawlUserProfile, similar_user)

    except:
        print('traceback : ', traceback.format_exc())

    if crawlUserProfile == None:
        try:
            crawlUserProfile = CrawlUserProfile.objects.get(username=username)
        except:
            print('traceback : ', traceback.format_exc())

    return crawlUserProfile

def savePost(shortcode, result_post_json, crawlRecord=None):
    try:
        if 'is_not_found' in result_post_json:
            return None

        if crawlRecord == None:
            crawlRecord = CrawlRecord()
            crawlRecord.from_source = 2
            crawlRecord.save()

        # print('Save Dataset')
        dataSet = InstagramCrawlerDataSet(crawlRecord)
        # print('Save CrawlUser')
        # crawlUserProfile = dataSet.saveCrawlUser(result_post_json['user'])
        crawlUserProfile, is_created = CrawlUserProfile.objects.get_or_create(insta_pk=result_post_json['user']['pk'])
        # print('Save CrawlPost')
        if crawlUserProfile.username == None and 'username' in result_post_json['user'] or is_created:
            crawlUserProfile.username = result_post_json['user']['username']
            crawlUserProfile.save()

        return_post = dataSet.saveCrawlPost(crawlUserProfile, result_post_json)
        # print('Done')
        if 'comments' in result_post_json:
            comments = result_post_json['comments']
            for comment in comments:
                print("save Comment")
                dataSet.saveCrawlPostComment(return_post, comment)
        print('complete')


    except:
        print('savePost traceback : ', traceback.format_exc())


def savePostLiker(post_id, result_post_liker_json, crawlRecord=None):
    try:
        if 'is_not_found' in result_post_liker_json:
            return None

        if crawlRecord == None:
            crawlRecord = CrawlRecord()
            crawlRecord.from_source = 2
            crawlRecord.save()

        dataSet = InstagramCrawlerDataSet(crawlRecord)
        try:
            crawlPost = CrawlPost.objects.get(insta_pk = post_id)
        except:
            return

        users = result_post_liker_json['users']

        for index, like_user in enumerate(users):
            dataSet.saveCrawlPostLiker(crawlPost, like_user)


    except:
        print('traceback : ', traceback.format_exc())


'''
 람다 콜백 저장
'''
# 이걸 기준으로 ajax_save_crawler 만들기
# method를 더 만드는 것이 아닌 아래 분기를 추가할 것
@csrf_exempt
def lambda_save_crawler(request, received_json=None):
    """
        Args:
            received_json - {'event' : {'uesrname' : username}, 'data' : response}
    """
    if received_json != None:
        received_json_data = received_json
    else:
        received_json_data = json.loads(request.body.decode('utf-8'))

    event = received_json_data['event']
    print('event : ', event)
    data = received_json_data['data']
    errorMessage = None
    try:
        crawlRecord = None
        if 'crawl_record_id' in event:
            crawlRecord = CrawlRecord.objects.get(pk=event['crawl_record_id'])

        if 'username' in event:
            saveCrawlUser(event['username'], data, crawlRecord)

        if 'tag' in event:
            saveFindTag(event['tag'], data, crawlRecord)

        if 'hashtag' in event:
            saveExploreTag(event['hashtag'], data, crawlRecord)

        if 'post' in event:
            savePost(event['post'], data, crawlRecord)

        if 'location_id' in event:
            saveLocation(event['location_id'],  data, crawlRecord)

        if 'post_like' in event:
            savePostLiker(event['post_like'], data, crawlRecord)


    except:
        errorMessage = traceback.format_exc()


    request_id = event['request_id']
    try:
        eventRequest = LambdaFunctionEventRequest.objects.get(pk=request_id)
        print('eventRequest : ', eventRequest)
        if 'errorMessage' in data:
            eventRequest.is_error = True
            eventRequest.error_message = data['errorMessage']
        elif errorMessage != None:
            eventRequest.error_message = errorMessage
            eventRequest.is_error = True

        if eventRequest.is_error == True and 'is_not_found' not in data:
            lambda_status = eventRequest.lambda_status
            if lambda_status != None:
                lambda_status.onError(eventRequest.error_message)
                lambda_status.is_error = True
                lambda_status.save()

        eventRequest.complete_at = datetime.now()
        eventRequest.save()
    except:
        print('traceback', traceback.format_exc())
    return HttpResponse('success')


def amode_to_save_crawler(data=None):
    """
    A_Mode -> 저장
    request_type - user,post,hashtag
    """
    url = ''

    if 'graphql' in data:  #A_mode 원형데이터 저장
        graphql = data['graphql']
        if 'user' in graphql:
            data = {'user_data': graphql}
        elif 'shortcode_media' in graphql:
            data = {'post_data': graphql}
        elif 'hashtag' in graphql:
            data = {'hashtag_data': graphql}

    if 'username' in data and 'full_name' in data and 'id' in data: #유저 데이터만 저장 
        data = {'user_data': {'user': data}} 
        

    infoscraper = InstagramInfoScraper()

    try:
        if 'user_data' in data:
            data = data['user_data']
            userinfo = infoscraper.getUserInfo(url, a_mode=True, is_tor=False, crawl_type=1, data=data)
            print(data, userinfo)
            saveCrawlUser(data['user']['username'], userinfo)

        # if 'tag' in data:
        #     saveFindTag(event['tag'], data)

        if 'hashtag_data' in data:
            hashtag = infoscraper.exploreTags(json_result_data=data['hashtag_data'])
            saveExploreTag(hashtag['name'], hashtag)

        if 'post_data' in data:
            data = data['post_data']
            postinfo = infoscraper.getPost(url=url, node=data['shortcode_media'])
            savePost(data['shortcode_media']['shortcode'], postinfo)

        # if 'location_id' in data:
        #     saveLocation(event['location_id'], data)
        #
        # if 'post_like' in data:
        #     savePostLiker(event['post_like'], data)

        # print('end_saveCrawl')
    except:
        errorMessage = traceback.format_exc()
        print('errorMessage : ', errorMessage)

@csrf_exempt
def ajax_save_crawler(request):
    if request.method == 'POST':
        # print(request.body.decode('utf-8'))
        data = json.loads(request.body.decode('utf-8'))
        
        amode_to_save_crawler(data)
        return HttpResponse(status=200)
    return HttpResponse(status=400)

