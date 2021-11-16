class FeaturingEngineRouter:

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'instagram_crawler':
            return 'score_crawler_read'

        if model._meta.app_label == 'youtube_crawler':
            return 'score_crawler_youtube_read'

        if model._meta.app_label == 'tiktok_crawler':
            return 'score_crawler_tiktok'

        if model._meta.app_label == 'xiaohongshu_crawler':
            return 'score_xiaohongshu'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'instagram_crawler':
            return 'score_crawler_writer'

        if model._meta.app_label == 'youtube_crawler':
            return 'score_crawler_youtube_writer'

        if model._meta.app_label == 'tiktok_crawler':
            return 'score_crawler_tiktok'

        if model._meta.app_label == 'xiaohongshu_crawler':
            return 'score_xiaohongshu'


        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'instagram_crawler':
            return db == 'score_crawler_writer'

        if app_label == 'youtube_crawler':
            return db == 'score_crawler_youtube_writer'

        if app_label == 'tiktok_crawler':
            return db == 'score_crawler_tiktok'

        if app_label == 'xiaohongshu_crawler':
            return db == 'score_xiaohongshu'

        if app_label == 'auth' or app_label == 'admin' or app_label == 'contenttypes' \
            or app_label == 'sessions':

            return db == 'default'

        return None
