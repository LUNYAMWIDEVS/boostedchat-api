from .models import SandBoxChannel
from .models import WhatsappChannel
from .models import LinkedInChannel
from .models import InstagramChannel

class Channel:
    def __init__(self):
        pass 

    """
    channel is a string
    user is an object with {username, status1, status2, status3}
    """
    def addUser(channel, user):
        # save user to channel
        if channel == "whatsapp":
            WhatsappChannel.addUser(user)
        elif channel == "instagram":
            InstagramChannel.addUser(user)
        elif channel == "linkedin":
            LinkedInChannel.addUser(user)
        elif channel == "sandbox":
            SandBoxChannel.addUser(user)
        else:
            raise Exception("Channel not found")
        
    def editUser(channel, user):
        # edit user in channel
        if channel == "whatsapp":
            WhatsappChannel.editUser(user)
        elif channel == "instagram":
            InstagramChannel.editUser(user)
        elif channel == "linkedin":
            LinkedInChannel.editUser(user)
        elif channel == "sandbox":
            SandBoxChannel.editUser(user)
        else:
            raise Exception("Channel not found")
