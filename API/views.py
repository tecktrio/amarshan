'''
This logic part is developed by amal benny. For any doughts you can contact bshootdevelopers@gmail.com
'''

# Neccessary Modules for this app

import os
import smtplib
import time
import threading
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from API.models import Featured
from API.models import Users
from API.models import Products
from API.models import Categories
from API.models import Notification
from API.models import Donation_categories
from API.models import Donations
from API.models import Login_details

from API.serializers import DonationContent_Serializer
from API.serializers import FeaturedContent_Serializer
from API.serializers import User_Serializer
from API.serializers import Product_Serializer
from API.serializers import Category_Serializer
from API.serializers import Donation_category_serializer
from API.serializers import Notification_serializer
from API.serializers import User_Address_Serializer
from API.models import Orders
from API.serializers import Order_Serializer

from project_amarsha.settings import EMAIL_HOST_USER
from project_amarsha.settings import ACCESS_TOKEN_FACEBOOK_PAGE
from project_amarsha.settings import FACEBOOK_PAGE_ID
from project_amarsha.settings import INSTAGRAM_BUSINESS_ACCOUNT_ID

from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.shortcuts import render


def error_404(request,e):
    return render(request,'error/404.html')
def error_500(request):
    return render(request,'error/500.html')

'''
API for Amarshan a whole new platform for donations
---------------------------------------------------
'''

class root(APIView):
    def get(self,request):
        return JsonResponse({'welcome to amarshan api. please contact bshootdevelopers@gmail.com for any help, endpoints of this url for testing : email, login, signup, donations, upload, featured'})
    def post(self,request):
        return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})

# Debugging
class Login(APIView):
    '''
    Handles
    -------
    1. Login Request from Normal users
    2. Validate the Login details
    3. Verify the data 
    4. Send proper Response for errors
    5. store the login status of users
    '''
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            login_type = request.data['login_type']
            # device = request.data['device']
        except:
            return JsonResponse({'Required fields':'email, password, login_type'})
        if login_type == 'swe':
            if Users.objects.filter(email=email).exists():
                user= Users.objects.get(email=email)
                if user.password == password:
                    serialized_user_data = User_Serializer(user)
                    # storing the login details 
                    device = request.device
                    
                    Login_details.objects.create(email = email,device =device).save()
                    return JsonResponse({'status_code':'success','user':serialized_user_data.data})
                return JsonResponse({'status_code':'failed','error':'incorrect password'})
            return JsonResponse({'status_code':'failed','error':'user email id does not exist'})
        elif login_type == 'swg':
            if Users.objects.filter(email=email).exists():
                user= Users.objects.get(email=email)
                serialized_user_data = User_Serializer(user)
                Login_details.objects.create(email = email).save()
                return JsonResponse({'status_code':'success','user':serialized_user_data.data})
    def get(self,request):
                return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})            
    def put(self,request):
                return JsonResponse({'you are just a kid, you are not allowed to send a put request to this url'})
    def delete(self,request):
                return JsonResponse({'you are just a kid, you are not allowed to send a delete request to this url'})
            
            
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
                return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})
    def put(self,request,email_id):
        if Users.objects.filter(email=email_id).exists():
            try:
                display_name = request.data['display_name']
                # email= request.data['email']
                password= request.data['password']
                profile_url = request.data['profile_url']
                # login_type = request.data['login_type']
            except:
                return JsonResponse({'Required fields :':'display_name, password, profile_url'})
            user  =  Users.objects.get(email=email_id)
            user.display_name = display_name
            # user.email = email
            user.password = password
            user.profile_url = profile_url
            # user.login_type = login_type
            user.save()
            return JsonResponse({'status_code':'success','status':'user profile updated'})
        else:
            return JsonResponse({'status_code':'failed','error':'email id do not exist'})
    def delete(self,request):
                return JsonResponse({'you are just a kid, you are not allowed to send a delete request to this url'})
            
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
                return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})
    def delete(self,request):
                return JsonResponse({'you are just a kid, you are not allowed to send a delete request to this url'})
            
#Endpoint to Upload File
class Donation_content(APIView):
    def get(self,request):
        
        # print(request.mysecret_value)
        donation_content = Donations.objects.all()
        serialized_content = DonationContent_Serializer(donation_content,many = True)
        return JsonResponse({"donation_content":serialized_content.data})

    def put(self,request,id):
        try:
            current_amount = int(request.data['current_amount'])
            heart = int(request.data['heart'])
        except:
            return JsonResponse({'Required fields :':'current_amount, heart'})
        
        if Donations.objects.filter(id=id).exists():
            try:
                current_donation = Donations.objects.get(id=id)
                current_donation.current_amount = current_amount
                current_donation.heart = heart
                current_donation.save()
                return JsonResponse(({'status_code':'success','status':'donation upated'}))
            except:
                
                return JsonResponse(({'status_code':'failed','error':'could not save, invalid data'}))
        else:
            return JsonResponse(({'status_code':'failed','error':'id does not exist'}))
        
    def delete(self,request,id):
        if Donations.objects.filter(id=id).exists():
            Donations.objects.filter(id=id).delete()
            return JsonResponse({'status_code':'success','status':'Donation added successfully'})
        else:
            return JsonResponse({'status_code':'failed','error':'Donation id does not exist'})
        
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
            return JsonResponse({'status_code':'failed','Required fields':'media_url, profile_image_url, profile_username, organisation, descripton, location'})
        Featured.objects.create(media_url=media_url,profile_image_url=profile_image_url,profile_username=profile_username,organisation=organisation,description=description,location=location).save()
        return JsonResponse({"status":"done",'status_code':'success'})
    def get(self,request):
        featured_content = Featured.objects.all()
        serialized_content = FeaturedContent_Serializer(featured_content,many=True)
        return JsonResponse({"featured_content":serialized_content.data,'status_code':'success'})
    def put(self,request,id):
        if Featured.objects.filter(id=id).exists():
            try:
                featured_content = Featured.objects.all()
                featured_content.update(running_status = False)
                this_content = Featured.objects.get(id = id)
                this_content.running_status = True
                this_content.save()
            except:
                return Response({'status_code':'failed','error':'unknown error, could not save the changes'})
            return JsonResponse({'status':'featured content updated or changed','status_code':'success'})
        else:
            return JsonResponse({'status_code':'failed','status':'please provide a valid id'})
    def delete(self,request,id):
        if Featured.objects.filter(id=id).exists():
            try:
                Featured.objects.get(id=id).delete()
                return JsonResponse({'status_code':'success','status':'content deleted successfully'})
            except:
                return JsonResponse({'status_code':'failed','error':'unkown error, could not delete'})
        else:
            return JsonResponse({'status_code':'failed','error':'id does not exist'})
        
        
class Upload(APIView):
    throttle_classes = [UserRateThrottle]
    status = False
    
    def post(self,request):
        '''Listen to post request to the upload endpoint
        required parameter  :
        => VIDEO  : platform, media_type, video_url, title, description, tag
        => IMAGE  : platform, media_type, image, caption
        '''
        try:
            platform = request.data['platform']
            media_type = str(request.data['media_type']).upper()
            category = request.data['category']
            location = request.data['location']
            media_url = request.data['media_url']
            title = request.data['title']
            description = request.data['description']
            target = int(request.data['target'])
            
            if not Donation_categories.objects.filter(name=category).exists():
                return JsonResponse({'status_code':'failed','error':'category do not exist'})
            
            platform_list = platform.split(',')
        except:
            return JsonResponse({'Required fields':'platform, media_type, category, location, media_url, title, description, target'})
        
        
        social_media = Social_Media()
        
        if media_type == "VIDEO":
            if 'instagram' in platform_list:
                try:
                    self.status = social_media.Upload_video_to_instagram(media_url,title)
                except:
                    if not self.status:
                        return Response({'status':'failed','error':'video could not upload to instagram'})
            if 'facebook' in platform_list:
                try:
                    self.status = social_media.Upload_video_to_facebook(media_url,title,description)
                except:
                    if not self.status :
                        return Response({'status':'failed','error':'video could not upload to facebook or limit exceed'})
            if 'youtube' in platform_list:
                try:
                    self.status = social_media.Upload_video_to_youtube(media_url,title,description,category) 
                except:
                    if not self.status :
                        return Response({'status':'failed','error':'video could not upload to youtube or limit exceed'})
            if 'amarshan' in platform_list:
                self.status = social_media.Upload_video_to_amarshan(media_url,title,description,category,location, target) 
                
        elif media_type == "IMAGE":
            if 'instagram' in platform_list:
                try:
                    self.status = social_media.Upload_image_to_instagram(image_url=media_url,caption=title)
                except:
                    if not self.status:
                        return Response({'status':'failed','error':'image could not upload to instagram'})
            if 'facebook' in platform_list:
                try:
                    self.status = social_media.Upload_image_to_facebook(media_url,title )
                except:
                    if not self.status:
                        return Response({'status':'failed','error':'image could not upload to facebook'})
            if 'amarshan' in platform_list: 
                try:
                    self.status = social_media.Upload_image_to_amarshan(image_url=media_url,title=title,description = description,category = category,location=location,target=target) 
                except:
                    if not self.status:
                        return Response({'status':'failed','error':'image could not upload to amarshan'})
        # return true if video uploaded to all platforms
        if self.status:
            return JsonResponse({"status_code":'success','status':'donation content uploaded successfully'})
        else:
            return JsonResponse({"status_code":'failed'})
            

    def get(self,request):
        '''Listen to the get request for the endpoint upload'''
        return JsonResponse({"The method is not accessble. please try post using the fields :","For video => * video_url, * title, * description, * tag, * platform, * media type.","For Image =>* image, *caption, *platform, media_type"})
    
# Social Media access
'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
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
        return True
        
        
    '''
     uploading video
     -----------------------------------------------------------------------
    '''
    def Upload_video_to_instagram(self,video_url,title):
        '''Required parameter :
        => video_url, title
        '''
        if video_url is None:
            return JsonResponse({"Input Error":"video url cannot be empty and it should be valid"})
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
        return  True
    
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
            return False
        else:
            return True
        
    def Upload_video_to_youtube(self, video_url,title,description,tag):
        '''Required parameters
        => video_url, title, description, tag
        '''
        chuck_size = 256
        downloaded_video = requests.get(video_url,stream=True)
        print('downloading',end="")
        try:
            os.remove('live_yt.mp4')
        except:
            pass
        with open('live_yt.mp4',"wb") as f:
            for chunk in downloaded_video.iter_content(chunk_size=chuck_size):
                f.write(chunk)
                # print('.',end="")
        print('download is done -_-')
        run = f'py API/Important_file/upload_to_youtube.py  --title="{title}" --description="{description}" --keywords="{tag}"  --file="live_yt.mp4" '
        print(run)
        os.system(run)
        return True
    
    def Upload_video_to_amarshan(self, video_url,title,description,category,location,target):
        try:
            Donations.objects.create(
                media_url = video_url,
                media_type = 'VIDEO',
                title = title, 
                description = description,
                category = category,
                location=location,
                target = target
            ).save()
            return True
        except:
            return False

    '''
    Uploading image
    ----------------------------------------------------------------
    '''
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
            return False
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
            return True
        else:
            return False

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
            return True
        else:
            print('Error creating post:', response.json()['error']['message'])
            return False
        
    def Upload_image_to_amarshan(self,image_url, title, description, category,location,target):
        try:
            Donations.objects.create(
                media_url = image_url,
                media_type = 'IMAGE',
                title = title, 
                description = description,
                category = category,
                location = location,
                target = target
            ).save()
            return True
        except Exception as e:
            print(e)
            return False
        
   



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
            return JsonResponse({'status_code':'failed','Required fields':'name, description, category, rating, image_1_url, image_2_url, image_3_url, image_4_url, price'})
        try:
            if Products.objects.filter(name=name).exists():
                return JsonResponse({'status_code':'failed','status':'product name already exist','solution':'use another product name with some changes'})
            if not Categories.objects.filter(name=category).exists():
                return JsonResponse({'status_code':'failed','error':'category do not exist'})
            new_product = Products.objects.create(name=name,category=category,rating=rating,description=description,image_1_url=image_1_url,image_2_url=image_2_url,image_3_url=image_3_url,image_4_url=image_4_url,price=price)
            new_product.save()
        except:
            return JsonResponse({'status_code':'failed','error':'could not create the product, fields or data error while trying to save the new product'})
        return JsonResponse({'status':'new product added successfully','status_code':'success'})
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
                return JsonResponse({'status_code':'failed','Required fields':'name, description, category, rating, image_1_url, image_2_url, image_3_url, image_4_url, price'})
        
        
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
                return JsonResponse({'(status_code':'failed','error': str(e)})
            
            return JsonResponse({'status_code':'success','status':'product updated successfully'})
        else:
            return JsonResponse({'status_code':'failed','status':'The product id does not exists or product already deleted'})
    def delete(self,request,filter):
        if Products.objects.filter(id=filter).exists():
            Products.objects.get(id=filter).delete()
            return JsonResponse({'status_code':'success','status':'product deleted successfully'})
        else:
            return JsonResponse({'status_code':'failed','status':'The product id does not exists or product already deleted'})
        
class Handle_categories(APIView):
    def get(self,request):
        categories = Categories.objects.all()
        Serialized_categories = Category_Serializer(categories,many=True)
        return JsonResponse({'categories':Serialized_categories.data})
    def post(self,request):
        try:
            
            name = request.data['name']
            description = request.data['description']
            image_url = request.data['image_url']
        except Exception as e:
            return JsonResponse({'status_code':'failed','Required Fields' : 'name, description, image_url'})
        
        if Categories.objects.filter(name=name).exists():
            return JsonResponse({'status_code':'failed','status':'category already exist'})
        new_category = Categories.objects.create(name=name,description=description)
        new_category.save()
        
        return JsonResponse({'status_code':'success','status':'category created succesfully'})
    

class Handle_Donation_categories(APIView):
    def get(self,request):
        category = Donation_categories.objects.all()
        serialized_categories = Donation_category_serializer(category,many=True)
        return JsonResponse({'status_code':'successs','categories':serialized_categories.data})
    def post(self,request):
        try:
            name = request.data['name']
            description= request.data['description']
        except:
            return JsonResponse({'status_code':'failed','Required fields':'name, description'})
        if Donation_categories.objects.filter(name = name).exists():
            return JsonResponse({'status_code':'failed', 'error':'category already exist'})
        Donation_categories.objects.create(name=name, description= description).save()
        return JsonResponse({'status_code':'success','status':'category created successfully'})

class Handle_Notifications(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serialized_notifications = Notification_serializer(notifications,many=True)
        return JsonResponse({'status_code':'success','notifications':serialized_notifications.data})
    def post(self,request):
        try:
            try:
                title = request.data['title']
                message= request.data['message']
            except:
                return JsonResponse({'status_code':'failed','Required fields':'title , message'})
            
            if  Notification.objects.filter(title=title).exists():
                return JsonResponse({'status_code':'failed','status':'the notification with the same title already exist. '})
            new_request = Notification.objects.create(title = title, message = message)
            new_request.save()
            return JsonResponse({'status_code':'success','status':'notification created successfully'})
        except Exception as e:
            return JsonResponse({'status_code':'failed','error':e})
    def delete(self,request,id):
        if Notification.objects.filter(id=id).exists():
            try:
                Notification.objects.get(id=id).delete()
                return JsonResponse({'status_code':'success','status':'notification deleted succesfully'})
            except Exception as e:
                return JsonResponse({'status_code':'failed','error':e})
        else:
            return JsonResponse({'status_code':'failed','status':'notification id does not exist'})

class Handle_Address(APIView):
    def get(self,request,email_id):
        if Users.objects.filter(email = email_id).exists():
            user = Users.objects.get(email = email_id)
            user_address_serialized = User_Address_Serializer(user)
            return JsonResponse({'address':user_address_serialized.data,'status_code':'success'})
        else:
            return JsonResponse({'status':'email id does not exist','status_code':'failed'})
    def put(self,request,email_id):
            if Users.objects.filter(email = email_id).exists():
                user = Users.objects.get(email = email_id)
                try:
                    user.display_name = request.data['display_name']
                    user.building_name = request.data['building_name']
                    user.street_name  = request.data['street_name']
                    user.pincode   = request.data['pincode']
                    user.city = request.data['city']
                    user.state = request.data['state']
                    user.country = request.data['country']
                    user.landmark = request.data['landmark']
                    user.phone_number = request.data['phone_number']
                    user.save()
                    return JsonResponse({'status':'address updated succesfully','status_code':'success'})
                except:
                    return JsonResponse({'Required':'display_name, building_name, street_name, landmark, pincode, city, state, country, phone_number','status_code':'failed'})
                    
        
class Handle_myorders(APIView):
    def get(self,request,email_id):
        if Users.objects.filter(email = email_id).exists():
            orders = Orders.objects.filter(email_id=email_id)
            serialized_orders = Order_Serializer(orders,many= True)
            return JsonResponse({'status_code':'success','orders':serialized_orders.data})
        else:
            return JsonResponse({'status_code':'failed','error':' Invalide email id'})
    def post(self,request,email_id):
        if Users.objects.filter(email = email_id).exists():
            try:   
                product_name = request.data['product_name']
                product_description = request.data['product_description']
                product_price = request.data['product_price']
                product_image_url = request.data['product_image_url']
                item_count = request.data['item_count']
                ordered_on = request.data['ordered_on']
            except:
                return JsonResponse({'status_code':'failed','Required fields':'product_name, product_description, product_price, product_image_url, item_count, ordered_on'})
       
            try:
                Orders.objects.create(email_id=email_id, product_name=product_name, product_description=product_description, product_price=product_price, product_image_url=product_image_url,item_count = item_count,ordered_on=ordered_on).save()
                return JsonResponse({'status_code':'success','orders':'order places succesfully'})
            except Exception as e:
                return JsonResponse({'status_code':'failed','error':str(e)})
        else:
            return JsonResponse({'status_code':'failed','error':' Invalide email id'})
    def put(self,request,email_id,order_id):
        try:
            status = request.data['status']
        except:
            return JsonResponse({'status_code':'failed','Required':'status'})
        if Orders.objects.filter(id= order_id).exists():
            try:
                order = Orders.objects.get(id=order_id)
                if status not in  ['pending','ordered','cancelled','delivered','processing','shipping']:
                    raise TypeError
                order.order_status = status
                order.save()
                return JsonResponse({'status_code':'success','status':'status updated successfully'})
            except:
                return JsonResponse({'status_code':'failed','error':'status can only be pending, delivered, cancelled, shipping, ordered, processing '})
        else:
            return JsonResponse({'status_code':'failed','error':'order id does not exist'})