from enum import Enum

# code - label - minutes
class ServiceType(Enum):
    OIL = ("change_oil", "Change oil", 2)
    TIRES = ("inflate_tires", "Inflate tires", 5)
    DIAGNOSTIC = ("diagnostic", "Get diagnostic test", 30)

    def __init__(self, code, label, minutes):
        self.code = code
        self.label = label
        self.minutes = minutes

    @classmethod
    def get_by_code(cls, code):
        for service in cls:
            if service.code == code:
                return service
        return None
