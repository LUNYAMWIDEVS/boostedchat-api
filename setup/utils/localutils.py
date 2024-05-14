import os
from rest_framework.permissions import IsAuthenticated 

class setuputils:
    @staticmethod
    def get_permissions():
        if not os.environ.get('DEV_ENV') or os.environ.get('DEV_ENV') == 'False':
            return [IsAuthenticated]
        return []
    

    

