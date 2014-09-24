import base64
import hmac
import json
import time
import os
from hashlib import sha1
from hashlib import md5

from src.location import Location
from src.Yak import Yak
from src.comment import Comment
from src.peekLocation import PeekLocation
import requests


class Yakker:
    BASE_URL = "http://yikyakapp.com/api/"
    USER_AGENT = "android-async-http/1.4.4 (http://loopj.com/android-async-http)"

    def __init__(self, user_id=None, location=None, force_register=False):
        """

        :param user_id:
        :param location:
        :param force_register:
        :return:
        """
        if location is None:
            location = Location('0', '0')
        self.update_location(location)

        if user_id is None:
            user_id = self.gen_id()
            self.register_id_new(user_id)
        elif force_register:
            self.register_id_new(user_id)

        self.id = user_id

        self.handle = None

        # self.update_stats()

    def gen_id(self):
        """

        :return:
        """
        return md5(os.urandom(128)).hexdigest().upper()

    def register_id_new(self, id):
        """

        :param id:
        :return:
        """
        params = {
            "userID": id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        result = self.get("registerUser", params)
        return result

    def sign_request(self, page, params):
        """

        :param page:
        :param params:
        :return:
        """
        key = "35FD04E8-B7B1-45C4-9886-94A75F4A2BB4"

        # The salt is just the current time in seconds since epoch
        salt = str(int(time.time()))

        # The message to be signed is essentially the request, with parameters sorted
        msg = "/api/" + page
        sorted_params = params.keys()
        sorted_params.sort()
        if len(params) > 0:
            msg += "?"
        for param in sorted_params:
            msg += "%s=%s&" % (param, params[param])
        # Chop off last "&"
        if len(params) > 0:
            msg = msg[:-1]

        # the salt is just appended directly
        msg += salt

        # Calculate the signature
        h = hmac.new(key, msg, sha1)
        hash = base64.b64encode(h.digest())

        return hash, salt


    def get(self, page, params):
        """

        :param page:
        :param params:
        :return:
        """
        url = self.BASE_URL + page

        hash, salt = self.sign_request(page, params)
        params['hash'] = hash
        params['salt'] = salt

        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept-Encoding": "gzip",
        }

        return requests.get(url, params=params, headers=headers)

    def post(self, page, params):
        """

        :param page:
        :param params:
        :return:
        """
        url = self.BASE_URL + page

        hash, salt = self.sign_request(page, params)
        getparams = {'hash': hash, 'salt': salt}

        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept-Encoding": "gzip",
        }

        return requests.post(url, data=params, params=getparams, headers=headers)

    def get_yak_list(self, page, params):
        """

        :param page:
        :param params:
        :return:
        """
        return self.parse_yaks(self.get(page, params).text)

    def parse_yaks(self, text):
        """

        :param text:
        :return:
        """
        try:
            raw_yaks = json.loads(text)["messages"]
        except:
            raw_yaks = []
        yaks = []
        for raw_yak in raw_yaks:
            yaks.append(Yak(raw_yak, self))
        return yaks

    def parse_comments(self, text, message_id):
        """

        :param text:
        :param message_id:
        :return:
        """
        try:
            raw_comments = json.loads(text)["comments"]
        except:
            raw_comments = []
        comments = []
        for raw_comment in raw_comments:
            comments.append(Comment(raw_comment, message_id, self))
        return comments

    def contact(self, message):
        """

        :param message:
        :return:
        """
        params = {
            "userID": self.id,
            "message": message
        }
        return self.get("contactUs", params)

    def upvote_yak(self, message_id):
        """

        :param message_id:
        :return:
        """
        params = {
            "userID": self.id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("likeMessage", params)

    def downvote_yak(self, message_id):
        """

        :param message_id:
        :return:
        """
        params = {
            "userID": self.id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("downvoteMessage", params)

    def upvote_comment(self, comment_id):
        """

        :param comment_id:
        :return:
        """
        params = {
            "userID": self.id,
            "commentID": comment_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("likeComment", params)

    def downvote_comment(self, comment_id):
        """

        :param comment_id:
        :return:
        """
        params = {
            "userID": self.id,
            "commentID": comment_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("downvoteComment", params)

    def report_yak(self, message_id):
        """

        :param message_id:
        :return:
        """
        params = params = {
            "userID": self.id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("reportMessage", params)

    def delete_yak(self, message_id):
        """

        :param message_id:
        :return:
        """
        params = {
            "userID": self.id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("deleteMessage2", params)

    def report_comment(self, comment_id, message_id):
        """

        :param comment_id:
        :param message_id:
        :return:
        """
        params = {
            "userID": self.id,
            "commentID": comment_id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("reportMessage", params)

    def delete_comment(self, comment_id, message_id):
        """

        :param comment_id:
        :param message_id:
        :return:
        """
        params = {
            "userID": self.id,
            "commentID": comment_id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get("deleteComment", params)

    def get_greatest(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get_yak_list("getGreatest", params)

    def get_my_tops(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get_yak_list("getMyTops", params)

    def get_recent_replied(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get_yak_list("getMyRecentReplies", params)

    def update_location(self, location):
        """

        :param location:
        :return:
        """
        # @Warning self.location is defined outside init
        self.location = location

    def get_my_recent_yaks(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get_yak_list("getMyRecentYaks", params)

    def get_area_tops(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get_yak_list("getAreaTops", params)

    def get_yaks(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.get_yak_list("getMessages", params)

    def post_yak(self, message, show_loc=False, handle=False):
        """

        :param message:
        :param showloc:
        :param handle:
        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
            "message": message,
        }
        if not show_loc:
            params["hidePin"] = "1"
        if handle and (self.handle is not None):
            params["hndl"] = self.handle
        return self.post("sendMessage", params)

    def get_comments(self, message_id):
        """

        :param message_id:
        :return:
        """
        params = {
            "userID": self.id,
            "messageID": message_id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }

        return self.parse_comments(self.get("getComments", params).text, message_id)

    def post_comment(self, message_id, comment):
        """

        :param message_id:
        :param comment:
        :return:
        """
        params = {
            "userID": self.id,
            "messageID": message_id,
            "comment": comment,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        return self.post("postComment", params)

    def get_peek_locations(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        data = self.get("getMessages", params).json()
        peeks = []
        for peek_json in data['otherLocations']:
            peeks.append(PeekLocation(peek_json))
        return peeks

    def get_featured_locations(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        data = self.get("getMessages", params).json()
        peeks = []
        for peek_json in data['featuredLocations']:
            peeks.append(PeekLocation(peek_json))
        return peeks

    def get_yakarma(self):
        """

        :return:
        """
        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
        }
        data = self.get("getMessages", params).json()
        return int(data['yakarma'])

    def peek(self, peek_id):
        """

        :param peek_id:
        :return:
        """
        if isinstance(peek_id, PeekLocation):
            peek_id = peek_id.id

        params = {
            "userID": self.id,
            "lat": self.location.latitude,
            "long": self.location.longitude,
            'peekID': peek_id,
        }
        return self.get_yak_list("getPeekMessages", params)
