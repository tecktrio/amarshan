import os
import smtplib
import time
import threading
from django.shortcuts import redirect
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
from API.models import Products
from API.serializers import Product_Serializer
from API.models import Categories
from API.serializers import Category_Serializer
from project_amarsha.settings import EMAIL_HOST_USER
from project_amarsha.settings import ACCESS_TOKEN_FACEBOOK_PAGE,  FACEBOOK_PAGE_ID, INSTAGRAM_BUSINESS_ACCOUNT_ID
# import boto3
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse

class root(APIView):
    def get(self,request):
        return Response({'welcome to amarshan api. please contact bshootdevelopers@gmail.com for any help, endpoints of this url for testing : email, login, signup, donations, upload, featured'})
    def post(self,request):
        return Response({'you are just a kid, you are not allowed to send a post request to this url'})
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
    def get(self,request):
                return Response({'you are just a kid, you are not allowed to send a post request to this url'})
        
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
    def get(self,request):
                return Response({'you are just a kid, you are not allowed to send a post request to this url'})
     
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
                try:
                    html_content = render_to_string('mail/otp.html',{'otp':message})
                except:
                    return JsonResponse({'error':'render to string error, mail not send','status_code':'failed'})
            if template_model == 'message':
                html_content = render_to_string('mail/message.html',{'message':message})
            text_content = strip_tags(html_content)
            
            try:
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    EMAIL_HOST_USER,
                    [recipient_email]
                )
            except:
                return JsonResponse({'error':'email error, mail not send','status_code':'failed'})
            
            try:
                email.attach_alternative(html_content,'text/html')
            except Exception:
                return JsonResponse({'email attachment failed'})
            
            email.send()
            
        except Exception as e:
            print(e)
            return JsonResponse({'error':'unkown error, mail not send','status_code':'failed'})
        return JsonResponse({'status':'mail send successfully','status_code':'success'})
    def get(self,request):
                return Response({'you are just a kid, you are not allowed to send a post request to this url'})
     
#Endpoint to Upload File
class Donation_content(APIView):
    def get(self,request):
        donation_content = Donations.objects.all()
        serialized_content = DonationContent_Serializer(donation_content,many = True)
        return JsonResponse({"donation_content":serialized_content.data})
    # def post(self,request):
    #     media_url = request.data['media_url']
    #     media_type = request.data['media_type']
    #     target = request.data['target']
    #     title = request.data['title']
    #     description = request.data['description']
    #     location = request.data['location']
    #     donation_type = request.data['donation_type']
    #     Donations.objects.create(media_url=media_url,media_type=media_type,target=target,title=title,description=description,location=location,donation_type=donation_type).save()
    #     return JsonResponse({'donation_content':'done'})
    def put(self,request):
        try:
            field = request.data['field']
            id  = request.data['id']
            value = request.data['value']
        except:
            return JsonResponse({'Required fields :':'field, value, id'})
        
        if field == 'media_url':
            pass
        if field == 'media_type':
            pass
        if field == 'target':
            pass
        if field == 'title':
            pass
        if field == 'description':
            pass
        if field == 'location':
            pass
        if field == 'donation_type':
            pass
class Featured_content(APIView):
    def post(self,request):
        try:
            media_url = request.data['media_url']
            profile_image_url = request.data['profile_image_url']
            profile_username = request.data['profile_username']
            organisation = request.data['organisation']
            description = request.data['description']
            location = request.data['location']
            
        except:
            return Response({'status_code':'failed','Required fields':'media_url, profile_image_url, profile_username, organisation, descripton, location'})
        Featured.objects.create(media_url=media_url,profile_image_url=profile_image_url,profile_username=profile_username,organisation=organisation,description=description,location=location).save()
        return JsonResponse({"status":"done",'status_code':'success'})
    def get(self,request):
        featured_content = Featured.objects.filter(running_status = True)
        serialized_content = FeaturedContent_Serializer(featured_content,many=True)
        return JsonResponse({"featured_content":serialized_content.data,'status_code':'success'})
    def put(self,request,id):
        try:
            featured_content = Featured.objects.all()
            featured_content.update(running_status = False)
            this_content = Featured.objects.get(id = id)
            this_content.running_status = True
            this_content.save()
        except:
            return Response({'status_code':'failed','error':'add id of the featured image'})
        return JsonResponse({'status':'done','status_code':'success'})
    
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
                image_url = request.data['image_url']
                caption = request.data['caption']
            except:
                return JsonResponse({'Required fields':'image, caption'})
            
            # image_url = social_media.Upload_file_to_aws(image,title)
            
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



class Handle_Products(APIView):
    def get(self,request,filter):
        
        if filter == 'all':
            filter_result = Products.objects.all()
        else:
            #category filtering
            filter_result = Products.objects.filter(category=filter)
            
        serialized_data = Product_Serializer(filter_result,many=True)
        return Response({'products':serialized_data.data})
    def post(self,request):
        try:
            name = request.data['name']
            price =request.data['price']
            description = request.data['description']
            category = request.data['category']
            rating = request.data['rating']
            image_1_url = request.data['image_1_url']
            image_2_url = request.data['image_2_url']
            image_3_url = request.data['image_3_url']
            image_4_url = request.data['image_4_url']
        except:
            return Response({'status_code':'failed','Required fields':'name, description, category, rating, image_1_url, image_2_url, image_3_url, image_4_url, price'})
        try:
            if Products.objects.filter(name=name).exists():
                return Response({'status_code':'failed','status':'product name already exist','solution':'use another product name with some changes'})
            if not Categories.objects.filter(name=category).exists():
                return Response({'status_code':'failed','error':'category do not exist'})
            new_product = Products.objects.create(name=name,category=category,rating=rating,description=description,image_1_url=image_1_url,image_2_url=image_2_url,image_3_url=image_3_url,image_4_url=image_4_url,price=price)
            new_product.save()
        except:
            return Response({'status_code':'failed','error':'could not create the product, fields or data error while trying to save the new product'})
        return Response({'status':'new product added successfully','status_code':'success'})
    def put(self,request,filter):
        if Products.objects.filter(id=filter).exists():
            try:
                name = request.data['name']
                price =request.data['price']
                description = request.data['description']
                category = request.data['category']
                rating = request.data['rating']
                image_1_url = request.data['image_1_url']
                image_2_url = request.data['image_2_url']
                image_3_url = request.data['image_3_url']
                image_4_url = request.data['image_4_url']
            except:
                return Response({'status_code':'failed','Required fields':'name, description, category, rating, image_1_url, image_2_url, image_3_url, image_4_url, price'})
        
        
            try:
                product  = Products.objects.get(id=filter)
                product.name = name
                product.price = price
                product.description = description
                product.category = category 
                product.rating = rating
                product.image_1_url = image_1_url
                product.image_2_url = image_2_url
                product.image_3_url = image_3_url
                product.image_4_url = image_4_url
                
                product.save()
            except Exception as e:
                return Response({'(status_code':'failed','error': str(e)})
            
            return Response({'status_code':'success','status':'product updated successfully'})
        else:
            return Response({'status_code':'failed','status':'The product id does not exists or product already deleted'})
    def delete(self,request,filter):
        if Products.objects.filter(id=filter).exists():
            Products.objects.get(id=filter).delete()
            return Response({'status_code':'success','status':'product deleted successfully'})
        else:
            return Response({'status_code':'failed','status':'The product id does not exists or product already deleted'})
        
class Handle_categories(APIView):
    def get(self,request):
        categories = Categories.objects.all()
        Serialized_categories = Category_Serializer(categories,many=True)
        return Response({'categories':Serialized_categories.data})
    def post(self,request):
        try:
            name = request.data['name']
            description = request.data['description']
        except Exception as e:
            return Response({'status_code':'failed','Required Fields' : 'name, description'})
        
        if Categories.objects.filter(name=name).exists():
            return Response({'status_code':'failed','status':'category already exist'})
        new_category = Categories.objects.create(name=name,description=description)
        new_category.save()
        
        return Response({'status_code':'success','status':'category created succesfully'})