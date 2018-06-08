from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Inbox, Outbox
from django.conf import settings

import datetime

def index(request):
    return HttpResponse("OpenRoad API")

@csrf_exempt
def inbox(request):
    if request.method == 'POST':
        # Check for API Key
        if request.POST.get('api_key') and request.POST.get('api_key') == settings.API_KEY:
            # Receive values
            if request.POST.get('sender') and request.POST.get('body'):
                # Prepare a new inbox message
                inbox = Inbox()
                
                inbox.sender = request.POST.get('sender')
                inbox.body = request.POST.get('body')
                inbox.processed = 0

                inbox.save()

                message = "Message saved."
                response = JsonResponse({'message': message})
                response.status_code = 200
            else:
                message = "Pass message and sender."
                response = JsonResponse({'message': message})
                response.status_code = 404

            return response
        else:
            message = "UnAuthorized, Pass valid API Key."
            
            response = JsonResponse({'message': message})
            response.status_code = 403

            return response
    else: # request.method == 'GET'
        message = "Only POST allowed"
            
        response = JsonResponse({'message': message})
        response.status_code = 200

        return response

@csrf_exempt
def outbox(request):  
    if request.method == 'POST':
        # Check for API Key
        if request.POST.get('api_key') and request.POST.get('api_key') == settings.API_KEY:
            # Receive values
            if request.POST.get('text') and request.POST.get('to'):
                # Prepare a new outbox message
                outbox = Outbox()

                outbox.receiver = request.POST.get('to')
                outbox.body = request.POST.get('text')
                outbox.chat_found = 0
                outbox.processed = 0
                
                outbox.save()
                
                message = "Message saved."
                response = JsonResponse({'message': message})
                response.status_code = 200
            else:
                message = "Pass message and receiver."
                response = JsonResponse({'message': message})
                response.status_code = 404

            return response
        else:
            message = "UnAuthorized, Pass valid API Key."
            
            response = JsonResponse({'message': message})
            response.status_code = 403

            return response

    else: # request.method == 'GET'
        # Check for API Key
        if request.GET.get('api_key') and request.GET.get('api_key') == settings.API_KEY:
            # Fetching messages
            messages = []
            limit = 20

            try:
                outbox_messages = Outbox.objects.filter(processed=0)[:limit]

                for msg in outbox_messages:
                    messages += [{
                        'id': msg.id,
                        'receiver': msg.receiver,
                        'body': msg.body,
                        'chat_found': msg.chat_found,
                        'processed': msg.processed,
                        'processed_at': msg.processed_at,
                        'created_at': msg.created_at
                    }]
                
                status = 200

            except Outbox.DoesNotExist:
                status = 404
            
            response = JsonResponse({'status': status, 'messages': messages})
            response.status_code = status

            return response
        else:
            message = "UnAuthorized, Pass valid API Key."
            
            response = JsonResponse({'message': message})
            response.status_code = 403

            return response

@csrf_exempt
def update_outbox(request):
    if request.method == 'POST':
        # Check for API Key
        if request.GET.get('api_key') and request.GET.get('api_key') == settings.API_KEY:
            # Receive values
            if request.POST.get('message_id') and request.POST.get('chat_found') and request.POST.get('processed'):
                # Update message
                try:
                    outbox = Outbox.objects.get(id=request.POST.get('message_id'))

                    outbox.chat_found = request.POST.get('chat_found')
                    outbox.processed = request.POST.get('processed')
                    outbox.processed_at = datetime.datetime.now()

                    outbox.save()

                    status = 200
                    message = "Message updated."
                except Outbox.DoesNotExist:
                    status = 404
                    message = "Message not found."
                    
                response = JsonResponse({'status': status, 'message': message})
                response.status_code = status

            else:
                status = 404
                message = "Pass message id, chat found and processed status."

                response = JsonResponse({'status': status, 'message': message})
                response.status_code = status

            return response
        else:
            message = "UnAuthorized, Pass valid API Key."
            
            response = JsonResponse({'message': message})
            response.status_code = 403

            return response
    else: # request.method == 'GET'
        message = "Only POST allowed"
            
        response = JsonResponse({'message': message})
        response.status_code = 200

        return response