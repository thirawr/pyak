class Location:
    """
    Class made to represent a location.
    To Yak, we only need a lat and a long for this.
    """

    def __init__(self, latitude, longitude, delta=None):
        """
        Location Constructor

        :param latitude:
        :param longitude:
        :param delta:
        :return: Location Object
        """
        self.latitude = latitude
        self.longitude = longitude
        if delta is None:
            self.delta = "0.030000"
        else:
            self.delta = delta

    def __str__(self):
        return "Location(%s, %s)" % (self.latitude, self.longitude)