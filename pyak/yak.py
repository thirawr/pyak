import pyak.util as util


class Yak:
    """
    Main Yak class
    """

    def __init__(self, raw, client):
        """

        :param raw:
        :param client:
        :return:
        """
        self.client = client
        self.poster_id = raw["posterID"]
        self.hide_pin = bool(int(raw["hidePin"]))
        self.message_id = raw["messageID"]
        self.delivery_id = raw["deliveryID"]
        self.longitude = raw["longitude"]
        self.comments = int(raw["comments"])
        self.time = util.parse_time(raw["time"])
        self.latitude = raw["latitude"]
        self.likes = int(raw["numberOfLikes"])
        self.message = raw["message"]
        self.type = raw["type"]
        self.liked = int(raw["liked"])
        self.reyaked = raw["reyaked"]

        # Yaks don't always have a handle
        try:
            self.handle = raw["handle"]
        except KeyError:
            self.handle = None

        # For some reason this seems necessary
        self.message_id = self.message_id.replace('\\', '')

    def upvote(self):
        """

        :return:
        """
        if self.liked == 0:
            self.liked += 1
            self.likes += 1
            return self.client.upvote_yak(self.message_id)

    def downvote(self):
        """

        :return:
        """
        if self.liked == 0:
            self.liked -= 1
            self.likes -= 1
            return self.client.downvote_yak(self.message_id)

    def report(self):
        """

        :return:
        """
        return self.client.report_yak(self.message_id)

    def delete(self):
        """

        :return:
        """
        if self.poster_id == self.client.id:
            return self.client.delete_yak(self.message_id)

    def add_comment(self, comment):
        """

        :param comment:
        :return:
        """
        return self.client.post_comment(self.message_id, comment)

    def get_comments(self):
        """

        :return:
        """
        return self.client.get_comments(self.message_id)

    def print_yak(self):
        """

        :return:
        """
        if self.handle is not None:
            print "%s:" % self.handle
        print self.message
        print "%s likes, %s comments. posted %s at %s %s" % (
            self.likes, self.comments, self.time, self.latitude, self.longitude)
