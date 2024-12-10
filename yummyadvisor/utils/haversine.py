from django.db.models import Func, FloatField

class Haversine(Func):
    """
    Haversine function to calculate distance between two latitude/longitude points.
    """
    function = 'ACOS'
    template = (
        "ACOS(COS(RADIANS(%(latitude)s)) * COS(RADIANS(latitude)) * "
        "COS(RADIANS(%(longitude)s) - RADIANS(longitude)) + "
        "SIN(RADIANS(%(latitude)s)) * SIN(RADIANS(latitude))) * 6371"
    )  # 6371 is Earth's radius in kilometers

    def __init__(self, latitude, longitude, **extra):
        super().__init__(output_field=FloatField(), **extra)
        self.extra['latitude'] = latitude
        self.extra['longitude'] = longitude
