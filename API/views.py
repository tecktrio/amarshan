import os
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


# Create your views here.
class Upload_image_to_instagram(APIView):
    def post(self,request):
        
        page_id = 17841458772178702
        access_token = "EAALB1npj3f4BAJV9eTEliqxZApDwwscoZCVXpcqSOVcYcYZAd9BildIXjiluM5SedIg5OellwJGrkZAF99CBtWHHlpmbPqOWAMpE375SnsOob8JZCxc7IQYJjAGqzHEq7GutY1K7aQksc5ZBPTMNzOVM4dbnB98GmrcQwZBZBEJzBgurZBPTh7uZAB"
        image_url= request.data['image_url']
        get_url = "https://graph.facebook.com/v10.0/{}/media?image_url={}&access_token={}".format(page_id,image_url,access_token)
        print('Requesting for the image container id...')
        # print(get_url)
        response = requests.post(get_url)
        # print(response.json())
        image_container_id = int(response.json().get('id'))
        print('image container id  : ',image_container_id)
        print('Trying to upload the post...')
        post_url = "https://graph.facebook.com/v10.0/{}/media_publish?creation_id={}&access_token={}".format(page_id,image_container_id,access_token)
        response = requests.post(post_url)
        print('post id : ',response.json().get('id'))
        return Response(response)

class Upload_image_to_facebook(APIView):
    def post(self, request):

        # # Replace <access_token> with your actual access token
        access_token = "EAALB1npj3f4BABWQWptNPPg8jaRuj8cXP7tOquXrQ0VC5ZACmcZAN4WZAJ7n0ZCuEGNOT46zVRws3EJeAhlGsXZA97ZBYTtbdPPkfAFrB43tC1G89P0j7lzagE8Vt5TDiCRNmJZBur9soa9FoqEHErQdZBlCOt3SGMOp6j3SSADwnUIuDrvZAFv4jj9ZBpTRLydDoZD"
        # message = input('type the message to post : ')
        # post_url = 'https://graph.facebook.com/101183162938488/feed'
        image_url= request.data['image_url']
        caption = "this is the caption"
        # payload = {'access_token': access_token, 'message': 'Your message here'}
        import requests
        import os
        print('posting...')
        # posting message
        # response = requests.post("https://graph.facebook.com/101183162938488/feed?access_token={}&caption={}".format(access_token,message))
        # posting image
        page_id = 101200166274775
        response = requests.post(
            "https://graph.facebook.com/{}/photos?access_token={}&caption={}&url={}".format(page_id,access_token, caption, image_url))
        # bot.upload_photo(image_url,caption='this photo is from tecktrio bot')

        if response.status_code == 200:
            print('Post created successfully!')
        else:
            print('Error creating post:', response.json()['error']['message'])

        return Response({response})


class Upload_video_to_youtube(APIView):
    
    def post(self, request):
        title = "hello friends"
        file = 'yt2.mp4'
        description= 'common guys lets have fun'
        keywords = 'api test,api call'
        
        run = f'py API/tests.py  --title="{title}" --file="{file}" --description="{description}" --keywords="{keywords}"'
        print(run)
        os.system(run)
        return Response("done")
    
    
