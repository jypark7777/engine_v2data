import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import requests
import traceback
try:
    from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth
except:
    pass

"""
VERSION : 
2021.08.13 - Simiar 추가
"""

class InstagramInfoScraper:
    ctx = None
    DEVICE_SETTINTS = {'manufacturer': 'Xiaomi',
                       'model': 'HM 1SW',
                       'android_version': 19,
                       'android_release': '4.3'}
    USER_AGENT = 'Instagram 10.34.1 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**DEVICE_SETTINTS)


    def getPosts(self, edge_owner_to_timeline_media_json):
        posts = []

        if 'edges' in edge_owner_to_timeline_media_json:
            edges = edge_owner_to_timeline_media_json['edges']
            for edge in edges:
                try:
                    node = edge['node']
                    post = self.getPost(None,node=node)

                    posts.append(post)
                except:
                    print('post error : ' , traceback.format_exc())

        return posts


    def requestJson(self, url, is_tor=False):
        json_data = {}

        if is_tor:
            headers = {"User-Agent": self.USER_AGENT}
            response = ProxyRequests(url)
            response.set_headers(headers)
            response.get_with_headers()
            result = response.json
        else:
            headers = requests.utils.default_headers()
            headers.update(
                {
                    'User-Agent': self.USER_AGENT,
                }
            )
            response = requests.get(url, headers=headers)
            result = response.text

        if response.status_code == 404:
            json_data['is_not_found'] = True
            json_data['reponse'] = result
            return json_data
        try:
            if is_tor:
                json_data = result
            else:
                json_data = json.loads(result)

            return json_data
        except:
            json_data['is_error'] = True
            json_data['reponse'] = result
            json_data['errorMessage'] = traceback.format_exc()
            return json_data


    def getUserInfo(self, url, a_mode=True, is_tor=False, crawl_type=0, data=None):
        """

        crawl_type == 0 --> 기존 로직 그대로 (Request -> Save)
        crawl_type == 1 --> ajax로 a_mode 보낸 케이스 (Save)
        """
        json_data = {}
        user_data = {}

        if a_mode:
            if crawl_type == 0:
                data = self.requestJson(url, is_tor)
                if 'graphql' in data:
                    user_data = data['graphql']['user']
                else:
                    json_data['is_error'] = True
                    json_data['reponse'] = data
                    json_data['errorMessage'] = 'no graphql'
                    return json_data
            else:
                json_data = data
                user_data = json_data['user']
        else:
            html = urllib.request.urlopen(url, context=self.ctx).read()
            soup = BeautifulSoup(html, 'html.parser')

            body = soup.find('body')
            script = body.find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
            json_data = json.loads(raw)
            try:
                user_data = json_data['entry_data']['ProfilePage'][0]['graphql']["user"]
            except:
                json_data['is_error'] = True
                json_data['errorMessage'] = traceback.format_exc()
                return json_data

        try:

            userinfo = {}
            userinfo['pk'] = user_data["id"]
            userinfo['full_name'] = user_data["full_name"]
            userinfo['biography'] = user_data["biography"]
            userinfo['external_url'] = user_data["external_url"]
            userinfo['external_url_linkshimmed'] = user_data["external_url_linkshimmed"]
            userinfo['profile_pic_url'] = user_data["profile_pic_url"]
            userinfo['hd_profile_pic_url'] = user_data["profile_pic_url_hd"]
            userinfo['follower_count'] = user_data["edge_followed_by"]["count"]
            userinfo['following_count'] = user_data["edge_follow"]["count"]
            userinfo['followed_by_viewer'] = user_data["followed_by_viewer"]
            userinfo['follows_viewer'] = user_data["follows_viewer"]
            userinfo['has_channel'] = user_data["has_channel"]
            userinfo['has_blocked_viewer'] = user_data["has_blocked_viewer"]
            userinfo['blocked_by_viewer'] = user_data["blocked_by_viewer"]
            userinfo['has_requested_viewer'] = user_data["has_requested_viewer"]
            userinfo['requested_by_viewer'] = user_data["requested_by_viewer"]
            userinfo['connected_fb_page'] = user_data["connected_fb_page"]
            userinfo['country_block'] = user_data["country_block"]
            userinfo['highlight_reel_count'] = user_data["highlight_reel_count"]
            userinfo['is_joined_recently'] = user_data["is_joined_recently"]
            userinfo['is_verified'] = user_data["is_verified"]
            userinfo['is_private'] = user_data["is_private"]
            if 'is_business_account' in user_data:
                userinfo['is_business'] = user_data["is_business_account"]
            if 'is_professional_account' in user_data:
                userinfo['is_professional'] = user_data["is_professional_account"]
            userinfo['category_name'] = user_data["category_name"]

            append_keys = ['business_category_name', 'business_email', 'business_phone_number', 'category_enum']
            
            for append_key in append_keys:
                try:
                    if append_key in user_data:
                        userinfo[append_key] = user_data[append_key]
                except:
                    continue
            
            userinfo['posts'] = []
            if 'edge_owner_to_timeline_media' in user_data:
                userinfo['posts'] = self.getPosts(user_data['edge_owner_to_timeline_media'])
                userinfo['media_count'] = user_data["edge_owner_to_timeline_media"]["count"]
                userinfo['post_count'] = user_data["edge_owner_to_timeline_media"]["count"]
                
            if 'edge_felix_video_timeline' in user_data:
                userinfo['posts'].extend(self.getPosts(user_data['edge_felix_video_timeline']))

            if 'edge_related_profiles' in user_data:
                edge_related_profiles = user_data['edge_related_profiles']
                if 'edges' in edge_related_profiles and len(edge_related_profiles['edges']) > 0:
                    userinfo['similars'] = []
                    edge_related_profiles_edges = edge_related_profiles['edges']
                    for edge_related_profile in edge_related_profiles_edges:
                        edge_related_profile = edge_related_profile['node']
                        edge_related_profiles_user = {}
                        edge_related_profiles_user['pk'] = edge_related_profile['id']
                        edge_related_profiles_user['username'] = edge_related_profile['username']
                        try:
                            edge_related_profiles_user['profile_pic_url'] = edge_related_profile['profile_pic_url']
                            edge_related_profiles_user['is_verified'] = edge_related_profile['is_verified']
                            edge_related_profiles_user['is_private'] = edge_related_profile['is_private']
                            edge_related_profiles_user['full_name'] = edge_related_profile['full_name']
                        except:
                            pass
                        userinfo['similars'].append(edge_related_profiles_user)
                        
            
            return userinfo
        except:
            json_data['is_error'] = True
            json_data['errorMessage'] = traceback.format_exc()
            return json_data


    def getPost(self, url, sidecar_parent_id=None, node=None, is_tor=False):
        headers = requests.utils.default_headers()
        json_data = {}
        post_data = {}

        if node == None:
            data = self.requestJson(url, is_tor)
            if 'graphql' in data:
                post_data = data['graphql']['shortcode_media']
            else:
                json_data['is_error'] = True
                json_data['reponse'] = data
                json_data['errorMessage'] = 'no graphql'
                return json_data
        else:
            post_data = node

        try:
            post = {}
            post['sidecar_parent_id'] = sidecar_parent_id
            post['pk'] = post_data['id']
            if 'comments_disabled' in post_data:
                post['comment_threading_enabled'] = post_data['comments_disabled'] == False

            if '__typename' in post_data:
                post['typename'] = post_data['__typename']

            if 'edge_liked_by' in post_data:
                post['like_count'] = node['edge_liked_by']['count']
            elif 'edge_media_preview_like' in post_data:
                post['like_count'] = post_data['edge_media_preview_like']['count']

            if 'edge_media_to_comment' in post_data:
                post['comment_count'] = node['edge_media_to_comment']['count']

            if 'shortcode' in post_data:
                post['code'] = post_data['shortcode']

            if 'taken_at_timestamp' in post_data:
                post['taken_at'] = post_data['taken_at_timestamp']


            if 'edge_media_to_caption' in post_data:
                caption_edges =  post_data['edge_media_to_caption']['edges']
                if len(caption_edges) > 0:
                    caption = {}
                    caption['text'] = caption_edges[0]['node']['text']
                    post['caption'] = caption

            image_versions2 = {}
            image_versions2['candidates'] = []

            if 'owner' in post_data:
                owner_data = post_data['owner']
                post['user'] = {}
                post['user']['pk'] = owner_data['id']
                if 'username' in owner_data:
                    post['user']['username'] = owner_data['username']
                post['user_insta_pk'] = owner_data['id']

                try:
                    post['user']['profile_pic_url'] = owner_data['profile_pic_url']
                    post['user']['full_name'] = owner_data['full_name']
                    post['user']['is_private'] = owner_data['is_private']
                    post['user']['is_verified'] = owner_data['is_verified']
                except:
                    pass


            if 'thumbnail_resources' in post_data:
                for resource in post_data['thumbnail_resources']:
                    image_resource = {}
                    image_resource['url'] = resource['src']
                    image_resource['width'] = resource['config_width']
                    image_resource['height'] = resource['config_height']
                    image_versions2['candidates'].append(image_resource)

            if 'edge_media_to_tagged_user' in post_data:
                edge_media_to_tagged_user = post_data['edge_media_to_tagged_user']
                # print('edge_media_to_tagged_user : ', edge_media_to_tagged_user)
                edge_media_to_tagged_user_edges = edge_media_to_tagged_user['edges']
                post['usertags'] = {}
                post['usertags']['in'] = []

                for edge_media_to_tagged_user_edge in edge_media_to_tagged_user_edges:
                    edge_media_to_tagged_user_edge_node = edge_media_to_tagged_user_edge['node']
                    taged = {}
                    taged['user'] = edge_media_to_tagged_user_edge_node['user']
                    taged['user']['pk'] = edge_media_to_tagged_user_edge_node['user']['id']
                    taged['position'] = [edge_media_to_tagged_user_edge_node['x'], edge_media_to_tagged_user_edge_node['y']]
                    post['usertags']['in'].append(taged)
                    # print('taged : ', taged['user'])

            if 'is_video' in post_data:
                post['is_video'] = post_data['is_video']

            if 'location' in post_data:
                try:
                    location = {}
                    location['pk'] = post_data['location']['id']
                    location['name'] = post_data['location']['name']
                    location['address'] = post_data['location']['address_json']
                    post['location'] = location
                except:
                    pass

            if 'edge_media_to_parent_comment' in post_data:
                edge_media_to_parent_comment = post_data['edge_media_to_parent_comment']
                post['comment_count'] = edge_media_to_parent_comment['count']
                if post['comment_count'] > 0 and 'edges' in edge_media_to_parent_comment:
                    comments = []
                    comment_edges = edge_media_to_parent_comment['edges']
                    for comment_edge in comment_edges:
                        comment_edge_node = comment_edge['node']
                        comment = {}
                        comment['pk'] = comment_edge_node['id']
                        comment['text'] = comment_edge_node['text']
                        comment['created_at'] = comment_edge_node['created_at']
                        comment['comment_like_count'] = comment_edge_node['edge_liked_by']['count']
                        comment['user'] = {}
                        comment['user']['pk'] = comment_edge_node['owner']['id']
                        comment['user']['profile_pic_url'] = comment_edge_node['owner']['profile_pic_url']
                        comment['user']['username'] = comment_edge_node['owner']['username']
                        comments.append(comment)

                        edge_threaded_comments = comment_edge_node['edge_threaded_comments']
                        if edge_threaded_comments['count'] > 0 and 'edges' in edge_threaded_comments:
                            comment_thread_edges = edge_threaded_comments['edges']
                            for comment_thread_edge in comment_thread_edges:
                                comment_thread_edge_node = comment_thread_edge['node']
                                comment2 = {}
                                comment2['pk'] = comment_thread_edge_node['id']
                                comment2['text'] = comment_thread_edge_node['text']
                                comment2['created_at'] = comment_thread_edge_node['created_at']
                                comment2['comment_like_count'] = comment_thread_edge_node['edge_liked_by']['count']
                                comment2['user'] = {}
                                comment2['user']['pk'] = comment_thread_edge_node['owner']['id']
                                comment2['user']['profile_pic_url'] = comment_thread_edge_node['owner']['profile_pic_url']
                                comment2['user']['username'] = comment_thread_edge_node['owner']['username']
                                comments.append(comment2)

                    post['comments'] = comments

            if post_data['is_video'] == True:
                if 'display_url' in post_data and 'dimensions' in post_data:
                    video_versions = {}
                    video_versions['candidates'] = []

                    video_resource = {}
                    video_resource['url'] = post_data['display_url']
                    video_resource['width'] = post_data['dimensions']['width']
                    video_resource['height'] = post_data['dimensions']['height']
                    video_versions['candidates'].append(video_resource)

                    post['video_versions'] = video_versions
            else:
                if 'display_url' in post_data and 'dimensions' in post_data:
                    image_resource = {}
                    image_resource['url'] = post_data['display_url']
                    image_resource['width'] = post_data['dimensions']['width']
                    image_resource['height'] = post_data['dimensions']['height']
                    image_versions2['candidates'].append(image_resource)

            post['image_versions2'] = image_versions2

            if 'accessibility_caption' in post_data:
                post['accessibility_caption'] = post_data['accessibility_caption']

            if 'video_view_count' in post_data:
                post['video_view_count'] = post_data['video_view_count']


            if 'edge_sidecar_to_children' in post_data:
                post['sidecar_children'] = []
                edge_sidecar_to_children = post_data['edge_sidecar_to_children']
                sidecar_edges = edge_sidecar_to_children['edges']
                for sidecar_edge in sidecar_edges:
                    sidecar_post_data = sidecar_edge['node']
                    child_post = self.getPost(None, sidecar_parent_id=post['pk'], node=sidecar_post_data)
                    post['sidecar_children'].append(child_post)

        except:
            json_data['is_error'] = True
            json_data['errorMessage'] = traceback.format_exc()
            return json_data


        return post

    def getPostLike(self, post, is_tor=False):
        json_data = {}
        url = 'https://i.instagram.com/api/v1/media/%s/likers/?' % post
        result = None

        data = self.requestJson(url, is_tor)
        return data


    def searchTags(self, tag, is_tor=False):
        json_data = {}
        url = 'https://i.instagram.com/api/v1/tags/search/?is_typeahead=true&q=%s' % tag
        result = None

        data = self.requestJson(url, is_tor)
        if 'results' in data:
            return data['results']
        else:
            json_data['is_error'] = True
            json_data['reponse'] = result
            json_data['errorMessage'] = 'no results'
            return json_data


    def exploreLocations(self, url, is_tor=False):
        """위치 검색
        """
        headers = requests.utils.default_headers()
        json_data = {}

        data = self.requestJson(url, is_tor)
        if 'graphql' in data:
            location_data = data['graphql']['location']
        else:
            json_data['is_error'] = True
            json_data['reponse'] = result
            json_data['errorMessage'] = 'no results'
            return json_data

        try:

            location = {}
            location['id'] = location_data["id"]
            location['name'] = location_data["name"]

            if 'lat' in location_data:
                location['lat'] = location_data["lat"]

            if 'lng' in location_data:
                location['lng'] = location_data["lng"]

            if 'slug' in location_data:
                location['slug'] = location_data["slug"]

            if 'blurb' in location_data:
                location['blurb'] = location_data["blurb"]

            if 'website' in location_data:
                location['website'] = location_data["website"]

            if 'phone' in location_data:
                location['phone'] = location_data["phone"]

            if 'address_json' in location_data:
                location['address_json'] = location_data["address_json"]

            if 'profile_pic_url' in location_data:
                location['profile_pic_url'] = location_data["profile_pic_url"]

            if 'edge_location_to_media' in location_data:
                edge_location_to_media = location_data['edge_location_to_media']
                location['posts'] = self.getPosts(edge_location_to_media)

                if 'count' in edge_location_to_media:
                    location['media_count'] = edge_location_to_media['count']

            if 'edge_location_to_top_posts' in location_data:
                location['top'] = self.getPosts(location_data['edge_location_to_top_posts'])


            if 'address_json' in location_data:
                location['address_json'] = location_data['address_json']

            return location
        except:
            json_data['is_error'] = True
            json_data['errorMessage'] = traceback.format_exc()
            return json_data



    def exploreTags(self, url=None, is_tor=False, json_result_data=None):
        headers = requests.utils.default_headers()
        json_data = {}

        if url is not None:
            data = self.requestJson(url, is_tor)
            if 'graphql' in data:
                hashtag_data = data['graphql']['hashtag']
            else:
                json_data['is_error'] = True
                json_data['reponse'] = data
                json_data['errorMessage'] = 'no results'
                return json_data
        else:
            hashtag_data = json_result_data['hashtag']

        try:

            hashtag = {}
            hashtag['id'] = hashtag_data["id"]
            hashtag['name'] = hashtag_data["name"]

            if 'is_top_media_only' in hashtag_data:
                hashtag['is_top_media_only'] = hashtag_data["is_top_media_only"]

            if 'is_following' in hashtag_data:
                hashtag['is_following'] = hashtag_data["is_following"]

            if 'allow_following' in hashtag_data:
                hashtag['allow_following'] = hashtag_data["allow_following"]

            if 'edge_hashtag_to_media' in hashtag_data:
                hashtag['posts'] = self.getPosts(hashtag_data['edge_hashtag_to_media'])

            if 'edge_hashtag_to_top_posts' in hashtag_data:
                hashtag['top'] = self.getPosts(hashtag_data['edge_hashtag_to_top_posts'])


            if 'edge_hashtag_to_related_tags' in hashtag_data:
                edge_hashtag_to_related_tags = hashtag_data['edge_hashtag_to_related_tags']
                if 'edges' in edge_hashtag_to_related_tags:
                    hashtag['related_tags'] = edge_hashtag_to_related_tags['edges']

            return hashtag
        except:
            json_data['is_error'] = True
            json_data['errorMessage'] = traceback.format_exc()
            return json_data



    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE


def findUsername(username, a_mode=True, is_tor=False):
    infoscraper = InstagramInfoScraper()

    url = 'https://www.instagram.com/%s/' % username
    if a_mode:
         url = url + '?__a=1'
    userinfo = infoscraper.getUserInfo(url, a_mode=a_mode, is_tor=is_tor)

    return userinfo

def exploreTags(tag, is_tor=False):
    infoscraper = InstagramInfoScraper()

    url = 'https://www.instagram.com/explore/tags/%s/?__a=1' % tag
    taginfos = infoscraper.exploreTags(url, is_tor=is_tor)

    return taginfos

def exploreLocations(location_id, is_tor=False):
    infoscraper = InstagramInfoScraper()

    url = 'https://www.instagram.com/explore/locations/%s/?__a=1' % location_id
    locaionInfos = infoscraper.exploreLocations(url, is_tor=is_tor)

    return locaionInfos


def searchTags(tag, is_tor=False):
    infoscraper = InstagramInfoScraper()
    taginfos = infoscraper.searchTags(tag, is_tor=is_tor)

    return taginfos

def findPost(post, is_tor=False):
    infoscraper = InstagramInfoScraper()

    url = 'https://www.instagram.com/p/%s/?__a=1' % post
    taginfos = infoscraper.getPost(url, is_tor=is_tor)

    return taginfos

def findPostLike(post, is_tor=False):
    infoscraper = InstagramInfoScraper()
    postlikes = infoscraper.getPostLike(post, is_tor=is_tor)

    return postlikes


def lambda_handler(event, context):
    is_tor = True

    json_data = {}

    if 'is_tor' in event:
        is_tor = event['is_tor']

    if 'username' in event:
        json_data = findUsername(event['username'], a_mode=True, is_tor=is_tor)

    if 'tag' in event:
        json_data = searchTags(event['tag'], is_tor=is_tor)

    if 'hashtag' in event:
        json_data = exploreTags(event['hashtag'], is_tor=is_tor)
        print('hashtag : ', json_data)

    if 'post' in event:
        json_data = findPost(event['post'], is_tor=is_tor)

    if 'post_like' in event:
        json_data = findPostLike(event['post_like'], is_tor=is_tor)

    if 'ip_check' in event:
        public_ipadress = requests.get('https://api.ipify.org').text
        json_data['ip'] = public_ipadress

    if 'callback' in event:
        url = event['callback']
        data = {'event':event, 'data':json_data}
        headers = {'content-type': 'application/json'}
        r=requests.post(url, data=json.dumps(data), headers=headers)
        r.text

    return json_data
