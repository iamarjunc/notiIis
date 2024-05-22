from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def trigger_notification_api(request):
    # Assuming the device_token, message_title, and message_body are sent in the request
    # device_token = request.data.get('device_token', 'fTkDO8cFutFf2egy3erp5O:APA91bG0bTAXPrxItvbL1RLt25j7BQZqWlilYVrnJCuKmwcGJlQw48ZQh3ivv-er-_-LL0MWcNose3StMaeYQm6NVbAyx4KCEXVP8zQfeNIlhCykK-PuZU016P2-W_gb3nigVZ3vV6jP')  
    # message_title = request.data.get('msgTitle', 'hello there')
    # message_body = request.data.get('msgBody', 'this is mpower')

    device_token = request.data.get('device_token')  
    message_title = request.data.get('msgTitle')
    message_body = request.data.get('msgBody')
    if not device_token:
        return Response({'error': 'Device token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        image_url = request.data.get('imageUrl', 'http://192.168.7.2:555/static/images/OIG.png')
        send_notification(device_token, message_title, message_body, image_url)

        return Response({'message': 'Push notification triggered successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Failed to trigger push notification: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def send_notification(registration_ids, message_title, message_desc, image_url):
    fcm_api_key = "AAAA-IPj3Ss:APA91bGXMjGob_Qh4RQI2SsdlSGW7N-DPuHK4s5ZsqfUQDJRx9bD7OiYIl3_BQnR6LKrXIu9jP0OomnLtEKZNhtNzUTRDImS8cieqzvVI9Qi4BoT4uelECS9frw0rEGpNpS2elfpWC2u"

    
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={fcm_api_key}"
    }
    payload = {
        "to": registration_ids,
        "notification": {
            "title": message_title,
            "body": message_desc,
            "image": image_url
        }
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx status codes

        response_data = response.json()
        print("Notification sent successfully!")
        print(response_data)

    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")

        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.content}")

        # Handle specific error scenarios here

    except json.JSONDecodeError as je:
        print(f"Error decoding JSON response: {je}")