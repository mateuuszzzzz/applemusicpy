class AppleMusicException(Exception):
    pass

class AppleMusicClientException(AppleMusicException):
    pass

class AppleMusicAuthException(AppleMusicException):
    pass


class ResourceTypeException(AppleMusicClientException):
    pass