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
from API.models import Users
from API.serializers import User_Serializer
from project_amarsha.settings import EMAIL_HOST_USER
from project_amarsha.settings import ACCESS_TOKEN_FACEBOOK_PAGE,  FACEBOOK_PAGE_ID, INSTAGRAM_BUSINESS_ACCOUNT_ID
# import boto3
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse

class Login(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            login_type = request.data['login_type']
        except:
            return JsonResponse({'Required fields :':'email, password, login_type'})
        if login_type == 'swe':
            if Users.objects.filter(email=email).exists():
                user= Users.objects.get(email=email)
                if user.password == password:
                    serialized_user_data = User_Serializer(user)
                    return JsonResponse({'status_code':'success','user':serialized_user_data.data})
                return JsonResponse({'status_code':'failed','error':'incorrect password'})
            return JsonResponse({'status_code':'failed','error':'user email id does not exist'})
class SignUp(APIView):

    def post(self,request):
        try:
            display_name = request.data['display_name']
            email= request.data['email']
            password= request.data['password']
            profile_url = request.data['profile_url']
            login_type = request.data['login_type']
        except:
            return JsonResponse({'Required fields :':'display_name, email, password, profile_url, login_type'})
        
        user_exist_status = Users.objects.filter(email = email).exists()
        if not user_exist_status:
            Users.objects.create(display_name=display_name,email=email,password=password,profile_url=profile_url,login_type=login_type).save()
            return JsonResponse({'status':'user created successfully','status_code':'success'})
        else:
            return JsonResponse({"error":"user email id already exist.",'status_code':"failed"})
    
class Email(APIView):
    def post(self,request):
        try:
            subject = request.data['subject']
            message = request.data['message']
            recipient_email = request.data['recipient_email']
            template_model = request.data['template_model']
        except:
            return JsonResponse({'Required fields : ':'subject, message, recipient_email, template_model (otp, message)'})
        # email_from = EMAIL_HOST_USER
        # recipient_list = [recipient_email, ]
        # send_mail( subject, message, email_from, recipient_list )
        try:
            if template_model =='otp':
                html_content = render_to_string('mail/otp.html',{'otp':message})
            if template_model == 'message':
                html_content = render_to_string('mail/message.html',{'message':message})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject,
                text_content,
                EMAIL_HOST_USER,
                [recipient_email]
            )
            email.attach_alternative(html_content,'text/html')
            email.send()
        except:
            return JsonResponse({'error':'unkown error, mail not send','status_code':'failed'})
        return JsonResponse({'status':'mail send successfully','status_code':'success'})
        
#Endpoint to Upload File
class Donation_content(APIView):
    def get(self,request):
        donation_content = Donations.objects.all()
        serialized_content = DonationContent_Serializer(donation_content,many = True)
        return JsonResponse({"donation_content":serialized_content.data})
    def post(self,request):
        media_url = request.data['media_url']
        media_type = request.data['media_type']
        target = request.data['target']
        title = request.data['title']
        description = request.data['description']
        location = request.data['location']
        donation_type = request.data['donation_type']
        Donations.objects.create(media_url=media_url,media_type=media_type,target=target,title=title,description=description,location=location,donation_type=donation_type).save()
        return JsonResponse({'donation_content':'done'})
    
class Featured_content(APIView):
    def post(self,request):
        media_url = request.data['media_url']
        profile_image_url = request.data['profile_image_url']
        profile_username = request.data['profile_username']
        organisation = request.data['organisation']
        description = request.data['description']
        location = request.data['location']
        Featured.objects.create(media_url=media_url,profile_image_url=profile_image_url,profile_username=profile_username,organisation=organisation,description=description,location=location).save()
        return JsonResponse({"status":"done"})
    def get(self,request):
        featured_content = Featured.objects.filter(running_status = True)
        serialized_content = FeaturedContent_Serializer(featured_content,many=True)
        return JsonResponse({"featured_content":serialized_content.data})
    def put(self,request,id):
        featured_content = Featured.objects.all()
        featured_content.update(running_status = False)
        this_content = Featured.objects.get(id = id)
        this_content.running_status = True
        this_content.save()
        return JsonResponse({'status':'done'})
    
class Upload(APIView):
    throttle_classes = [UserRateThrottle]

    status = 'failed'
    def post(self,request):
        '''Listen to post request to the upload endpoint
        required parameter  :
        => VIDEO  : platform, media_type, video_url, title, description, tag
        => IMAGE  : platform, media_type, image, caption
        '''
        try:
            platform = request.data['platform']
            media_type = request.data['media_type']
            platform_list = platform.split(',')
        except:
            return Response({'Required fields':'platform, media_type'})
        social_media = Social_Media()
        
        if media_type == "VIDEO":
            try:
                video_url = request.data['video_url']
                title = request.data['title']
                description = request.data['description']
                tag = request.data['tag']
            except:
                return JsonResponse({"Required fields":"video_url, title, description, tag"})
            
            # video_url = social_media.Upload_file_to_aws(video_url,title)
            
            if 'instagram' in platform_list:
                self.status = social_media.Upload_video_to_instagram(video_url,title)
            if 'facebook' in platform_list:
                self.status = social_media.Upload_video_to_facebook(video_url,title,description)
            if 'youtube' in platform_list:
                self.status = social_media.Upload_video_to_youtube(video_url,title,description,tag) 
                
        elif media_type == "IMAGE":
            try:
                image = request.data['image']
                caption = request.data['caption']
            except:
                return JsonResponse({'Required fields':'image, caption'})
            
            image_url = social_media.Upload_file_to_aws(image,title)
            
            if 'instagram' in platform_list:
                self.status = social_media.Upload_image_to_instagram(image_url=image_url,caption=caption)
            if 'facebook' in platform_list:
                self.status = social_media.Upload_image_to_facebook(image_url,caption)
        return JsonResponse({"status":self.status})

    def get(self,request):
        '''Listen to the get request for the endpoint upload'''
        return JsonResponse({"The method is not accessble. please try post using the fields :","For video => * video_url, * title, * description, * tag, * platform, * media type.","For Image =>* image, *caption, *platform, media_type"})
    
# Social Media access
class Social_Media:
    def uploading_thread_method(self,video_container_id,access_token,page_id):
        count = 0
        while requests.get("https://graph.facebook.com/v10.0/{}?fields=status_code&access_token={}".format(video_container_id,access_token)).json().get('status_code')!="FINISHED":
            print(count, 'seconds',end='\r')
            count += 1
            time.sleep(1)

        print('Making the video public...')
        post_url = "https://graph.facebook.com/v10.0/{}/media_publish?creation_id={}&access_token={}".format(page_id,video_container_id,access_token)
        response = requests.post(post_url)
        print('post id : ',response.json().get('id'))
        return
        
    def Upload_video_to_instagram(self,video_url,title):
        '''Required parameter :
        => video_url, title
        '''
        if video_url is None:
            return Response({"Input Error":"video url cannot be empty and it should be valid"})
        page_id = INSTAGRAM_BUSINESS_ACCOUNT_ID #instagram bussiness account id
        access_token = ACCESS_TOKEN_FACEBOOK_PAGE
        get_url = "https://graph.facebook.com/v10.0/{}/media?video_url={}&caption={}&media_type={}&access_token={}".format(page_id,video_url,title,"VIDEO",access_token)
        print('Requesting for the video container id for instagram ...')
        response = requests.post(get_url)
        print(response.json())
        video_container_id = int(response.json().get('id'))
        if video_container_id is None:
            return JsonResponse({'status':'failed to get the container id from graph api'})
        print('Uploaded successfully...')
        print('image container id  : ',video_container_id)
        
        threading.Thread(target=self.uploading_thread_method,args=(video_container_id,access_token,page_id)).start()

        print("The video will be posted to instagram account successfully after completing the processing....")
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
        try:
            image_container_id = int(response.json().get('id'))
        except:
            return JsonResponse
        ({"Error":"some unkown error occured"})
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
        print('''****************** DEBUg ****************
        
        page id :''',page_id,'''
        video url : ''',video_url,'''
        title : ''',title,'''
        description : ''',description,'''
        ''')
        url = f"https://graph.facebook.com/{page_id}/videos"
        print('Trying to upload the post to facebook page...')
        data = {
            "file_url":video_url,
            "title":title,
            "description":description,
            "access_token":access_token
        }
        response = requests.post(url,json=data)
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
        chuck_size = 256
        downloaded_video = requests.get(video_url,stream=True)
        print('downloading',end="")
        os.remove('live_yt.mp4')
        with open('live_yt.mp4',"wb") as f:
            for chunk in downloaded_video.iter_content(chunk_size=chuck_size):
                f.write(chunk)
                print('.',end="")
        run = f'py API/Important_file/upload_to_youtube.py  --title="{title}" --description="{description}" --keywords="{tag}"  --file="live_yt.mp4" '
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


