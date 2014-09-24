from pyak import util

class Comment:
    """
    Comment Entity Class.
    This class represents a comment in the YikYak App
    """

    def __init__(self, raw, message_id, client):
        self.client = client
        self.message_id = message_id
        self.comment_id = raw["commentID"]
        self.comment = raw["comment"]
        self.time = util.parse_time(raw["time"])
        self.likes = int(raw["numberOfLikes"])
        self.poster_id = raw["posterID"]
        self.liked = int(raw["liked"])

        self.message_id = self.message_id.replace('\\', '')

    def upvote(self):
        """

        :return:
        """
        if self.liked == 0:
            self.likes += 1
            self.liked += 1
            return self.client.upvote_comment(self.comment_id)

    def downvote(self):
        """

        :return:
        """
        if self.liked == 0:
            self.likes -= 1
            self.liked -= 1
            return self.client.downvote_comment(self.comment_id)

    def report(self):
        """

        :return:
        """
        return self.client.report_comment(self.comment_id, self.message_id)

    def delete(self):
        """

        :return:
        """
        if self.poster_id == self.client.id:
            return self.client.delete_comment(self.comment_id, self.message_id)

    def reply(self, comment):
        """

        :param comment:
        :return:
        """
        return self.client.post_comment(self.message_id, comment)

    def print_comment(self):
        """

        :return:
        """
        my_action = ""
        if self.liked > 0:
            my_action = "^"
        elif self.liked < 0:
            my_action = "v"
        print "%s(%s) %s" % (my_action, self.likes, self.comment)
