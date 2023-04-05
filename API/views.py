import os
import time
import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
import requests
from API.models import Donations
from API.serializers import DonationContent_Serializer
from API.models import Featured
from API.serializers import FeaturedContent_Serializer
from project_amarsha.settings import ACCESS_TOKEN_FACEBOOK_PAGE,  FACEBOOK_PAGE_ID, INSTAGRAM_BUSINESS_ACCOUNT_ID
# import boto3
#Endpoint to Upload File
class Donation_content(APIView):
    def get(self,request):
        donation_type = request.POST.get('donation_type')
        donation_content = Donations.objects.filter(donation_type = donation_type)
        serialized_content = DonationContent_Serializer(donation_content,many = True)
        return Response({"donation_content":serialized_content.data})
    def post(self,request):
        media_url = request.data['media_url']
        media_type = request.data['media_type']
        target = request.data['target']
        title = request.data['title']
        description = request.data['description']
        location = request.data['location']
        donation_type = request.data['donation_type']
        Donations.objects.create(media_url=media_url,media_type=media_type,target=target,title=title,description=description,location=location,donation_type=donation_type).save()
        return Response({'donation_content':'done'})
    
class Featured_content(APIView):
    def post(self,request):
        media_url = request.data['media_url']
        profile_image_url = request.data['profile_image_url']
        profile_username = request.data['profile_username']
        organisation = request.data['organisation']
        description = request.data['description']
        location = request.data['location']
        Featured.objects.create(media_url=media_url,profile_image_url=profile_image_url,profile_username=profile_username,organisation=organisation,description=description,location=location).save()
        return Response({"status":"done"})
    def get(self,request):
        try:
            if request.data['isadmin'] == True:
                featured_content = Featured.objects.all()
                return Response({'featured data':featured_content})
        except:
            return Response({"status",'couldnt fetch the data,body should contain isadmin'})
        featured_content = Featured.objects.filter(running_status = True)
        serialized_content = FeaturedContent_Serializer(featured_content,many=True)
        return Response({"featured_content":serialized_content.data})
    def put(self,request,id):
        featured_content = Featured.objects.all()
        featured_content.update(running_status = False)
        this_content = Featured.objects.get(id = id)
        this_content.running_status = True
        this_content.save()
        return Response({'status':'done'})
    
class Upload(APIView):
    throttle_classes = [UserRateThrottle]

    status = 'failed'
    def post(self,request):
        '''Listen to post request to the upload endpoint
        required parameter  :
        => VIDEO  : platform, media_type, video_url, title, description, tag
        => IMAGE  : platform, media_type, image, caption
        '''
        platform = request.data['platform']
        media_type = request.data['media_type']
        platform_list = platform.split(',')
        social_media = Social_Media()
        
        if media_type == "VIDEO":
            video_url = request.data['video_url']
            title = request.data['title']
            description = request.data['description']
            tag = request.data['tag']
            
            # video_url = social_media.Upload_file_to_aws(video_url,title)
            
            if 'instagram' in platform_list:
                self.status = social_media.Upload_video_to_instagram(video_url,title)
            if 'facebook' in platform_list:
                self.status = social_media.Upload_video_to_facebook(video_url,title,description)
            if 'youtube' in platform_list:
                self.status = social_media.Upload_video_to_youtube(video_url,title,description,tag) 
                
        elif media_type == "IMAGE":
            image = request.data['image']
            caption = request.data['caption']
            
            image_url = social_media.Upload_file_to_aws(image,title)
            
            if 'instagram' in platform_list:
                self.status = social_media.Upload_image_to_instagram(image_url=image_url,caption=caption)
            if 'facebook' in platform_list:
                self.status = social_media.Upload_image_to_facebook(image_url,caption)
        return Response({"status":self.status})

    def get(self,request):
        '''Listen to the get request for the endpoint upload'''
        return Response({"The method is not accessble. please try post using the fields :","For video => * video_url, * title, * description, * tag, * platform, * media type.","For Image =>* image, *caption, *platform, media_type"})
    
# Social Media access
class Social_Media:
    def uploading_thread_method(self,video_container_id,access_token,page_id):
        while requests.get("https://graph.facebook.com/v10.0/{}?fields=status_code&access_token={}".format(video_container_id,access_token)).json().get('status_code')!="FINISHED":
            print('proccessing...')
            time.sleep(3)

        print('Making the video public...')
        post_url = "https://graph.facebook.com/v10.0/{}/media_publish?creation_id={}&access_token={}".format(page_id,video_container_id,access_token)
        response = requests.post(post_url)
        print('post id : ',response.json().get('id'))
        return
        
    def Upload_video_to_instagram(self,video_url,title):
        '''Required parameter :
        => video_url, title
        '''
        page_id = INSTAGRAM_BUSINESS_ACCOUNT_ID #instagram bussiness account id
        access_token = ACCESS_TOKEN_FACEBOOK_PAGE
        get_url = "https://graph.facebook.com/v10.0/{}/media?video_url={}&caption={}&media_type={}&access_token={}".format(page_id,video_url,title,"VIDEO",access_token)
        print('Requesting for the image container id...')
        response = requests.post(get_url)
        print(response.json())
        video_container_id = int(response.json().get('id'))
        print('Uploaded successfully...')
        print('image container id  : ',video_container_id)
        
        threading.Thread(target=self.uploading_thread_method,args=(video_container_id,access_token,page_id)).start()

        print("The video will be posted to facebook page successfully after completing the processing....")
        return 

    def Upload_image_to_instagram(self,image_url,caption):
        '''
        Required parameters :
        => image_url, caption
        '''
        page_id = INSTAGRAM_BUSINESS_ACCOUNT_ID #instagram bussiness account id
        access_token = ACCESS_TOKEN_FACEBOOK_PAGE
        get_url = "https://graph.facebook.com/v10.0/{}/media?image_url={}&access_token={}&caption={}".format(page_id,image_url,access_token,caption)
        print('Requesting for the image container id...')
        print('hitting on url : ',get_url)
        # print(get_url)
        response = requests.post(get_url)
        print(response.json())
        if response.json().get('id') is None:
            return 'failed'
        image_container_id = int(response.json().get('id'))
        print('image container id  : ',image_container_id)
        print('Trying to upload the post...')
        post_url = "https://graph.facebook.com/v10.0/{}/media_publish?creation_id={}&access_token={}".format(page_id,image_container_id,access_token)
        response = requests.post(post_url)
        print('post id : ',response.json().get('id'))
        if response.json().get('id') is not None:
            return 'success'
        else:
            return 'failed'

    def Upload_video_to_facebook(self,video_url,title,description):
        '''Required parameters
        => video_url, title, description
        '''
        page_id = FACEBOOK_PAGE_ID #facebook page id 
        access_token = ACCESS_TOKEN_FACEBOOK_PAGE
        url = "https://graph.facebook.com/v10.0/{}/videos?file_url={}&access_token={}&title={}&description={}".format(page_id,video_url,access_token,title,description)
        print('Trying to upload the post...')
        response = requests.post(url)
        print(response.json())
        print('post id : ',response.json().get('id'))
        if response.json().get('id') is None:
            return 'failed'
        else:
            return 'success'

    def Upload_image_to_facebook(self, image_url,caption):
        '''Required parameters :
        => image_url, caption
        '''
        access_token = ACCESS_TOKEN_FACEBOOK_PAGE
        page_id = FACEBOOK_PAGE_ID
        response = requests.post("https://graph.facebook.com/{}/photos?access_token={}&url={}".format(page_id,access_token, image_url))
        print(response.json())
        if response.status_code == 200:
            print('Post created successfully!')
            return 'success'
        else:
            print('Error creating post:', response.json()['error']['message'])
            return 'failed'
        
    def Upload_video_to_youtube(self, video_url,title,description,tag):
        '''Required parameters
        => video_url, title, description, tag
        '''
        run = f'py API/Important_file/upload_to_youtube.py  --title="{title}" --description="{description}" --keywords="{tag}"  --file="yt2.mp4" '
        print(run)
        os.system(run)
        return 'done'
    
    # def Upload_file_to_aws(self,file,file_name):
    #     client = boto3.client('s3',aws_access_key_id=AWS_CLIENT_ACCESS_KEY,aws_secret_access_key=AWS_CLIENT_SECRET_KEY)
    #     bucket_name = AWS_BUCKET_NAME
    #     client.upload_file(file, bucket_name, file_name)
    #     url = client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key':file_name})
    #     print('-'*30)
    #     print("your file is available at this url: ",url)
    #     print('-'*30)
    #     return url


