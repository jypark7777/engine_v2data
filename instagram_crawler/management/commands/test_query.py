from django.core.management.base import BaseCommand
from instagram_crawler.models import *
from instagram_crawler.documents import *

class Command(BaseCommand):

    def handle(self, **options):
        userProfile = CrawlUserProfile.objects.filter(username="orzlnee").last()
        # print(userProfile.username, userProfile.similar.all())

        # for sm in  userProfile.similar.all():
        #     print(sm.target_user.username)

        tags = CrawlSearchTag.objects.filter(posts__in=userProfile.crawlpost.all()).all()
        for tag in tags:
            print(tag)