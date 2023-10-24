from django.shortcuts import render

# Create your views here.
class DbCheckMiddleware(object):

    def process_request(self, request):
        try:
            "Some DB Code"
            success = True
        except:
            success = False                

        request.db_connection_successful = success