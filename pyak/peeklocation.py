from pyak.location import Location


class PeekLocation:
    """
    Peek Location Class
    TODO: Description
    """

    def __init__(self, raw):
        """
        Constructor

        :param raw: @Dictionary
        :return:
        """
        self.id = raw['peekID']
        self.can_submit = bool(raw['canSubmit'])
        self.name = raw['location']
        lat = raw['latitude']
        lon = raw['longitude']
        d = raw['delta']
        self.location = Location(lat, lon, d)