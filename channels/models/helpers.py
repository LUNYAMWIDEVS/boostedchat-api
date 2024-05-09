class helpers:

    @staticmethod
    def getChannelUserNameParams(params = {}, action = "read"):
        channel = params.get('channel', None)
        status1 = params.get('status1', None)
        status2 = params.get('status2', None)
        status3 = params.get('status3', None)
        username = params.get('username', None)
        sandbox = params.get('sandbox', False)
        if action == "read": # set default value for read
            if sandbox is None:
                sandbox = False
        return (channel, username, status1, status2, status3, sandbox)
    
    @staticmethod
    def channelsList():
        return ["whatsapp",  "sandbox", "linkedin", "instagram"]