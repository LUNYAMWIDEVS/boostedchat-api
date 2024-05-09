"""
These are helper functions put here to avoid circular imports
"""
from .linkedIn import *
from .sandbox import *
from .whatsapp import WhatsappUserNames
from .instagram import InstagramUserNames
class helpers_circular:

    @staticmethod
    def getChannelUserNameModel(channel):
        if channel == "instagram":
            return InstagramUserNames
        elif channel == "whatsapp":
            return WhatsappUserNames
        elif channel == "linkedin":
            return LinkedInUserNames
        elif channel == "sandbox":
            return SandboxUserNames
        return None
   