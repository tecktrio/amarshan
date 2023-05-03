'''
Author Details

Author: AMal Benny
Contact: amalpullan4@gmail.com

This logic part is developed by amal benny. For any doughts you can contact bshootdevelopers@gmail.com
'''

'''
API for Amarshan a whole new platform for donations  
---------------------------------------------------------------------------------------------------------------------
'''

# Neccessary Modules for this app
# run pip install -r requirement.txt to install the modules

import json
from modules import render
from modules import make_password
from modules import check_password
from modules import User_Wallet
from modules import User_Wallet_Serializer
from modules import JsonResponse
from modules import APIView
from modules import Users
from modules import User_Serializer
from modules import Login_details
from modules import render_to_string
from modules import datetime
from modules import strip_tags
from modules import send_mail
from modules import EMAIL_HOST_USER
from modules import Donations
from modules import DonationContent_Serializer
from modules import Donation_categories
from modules import Donation_category_serializer
from modules import Donation_Payment
from modules import Donation_History
from modules import Donation_History_Serializer
from modules import Featured
from modules import FeaturedContent_Serializer
from modules import Response
from modules import UserRateThrottle
from modules import requests
from modules import INSTAGRAM_BUSINESS_ACCOUNT_ID
from modules import FACEBOOK_PAGE_ID
from modules import ACCESS_TOKEN_FACEBOOK_PAGE
from modules import PASSWORD_ENCRYPTION_KEY
from modules import time
from modules import threading
from modules import os
from modules import Products
from modules import Product_Serializer
from modules import Categories
from modules import Category_Serializer
from modules import Notification
from modules import Notification_serializer
from modules import Categories
from modules import User_Address_Serializer
from modules import Orders
from modules import Order_Serializer
from modules import Login_details
from modules import Login_Detail_Serializer
from modules import Storage
from modules import Payment_Serializer


# Handling error pages in production environment
def error_404(request,e):
    return JsonResponse({'status':'page not fount, check the url'})
    # return render(request,'error/404.html')
def error_500(request):
    return JsonResponse({'status':'page not fount, check the url'})
    # return render(request,'error/500.html')

# handle root url
class root(APIView):
    def get(self,request):
        return JsonResponse({'welcome to amarshan api. please contact bshootdevelopers@gmail.com for any help, endpoints of this url for testing : email, login, signup, donations, upload, featured'})
    def post(self,request):
        return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})

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
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of user                                       #              
        #   password        :   valid password for new user                            #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            
            # collecting data from request
            email = request.data['email']
            _password = request.data['password']
            password = make_password(_password,PASSWORD_ENCRYPTION_KEY)
            login_type = request.data['login_type']
        except:
            
            # handle errors on data
            return JsonResponse({'Required fields':'email, password, login_type'})
        
        # handles login_type swe
        if login_type == 'swe':
            if Users.objects.filter(email=email).exists():
                user= Users.objects.get(email=email)
                if user.password == password:
                    user.password = _password
                    serialized_user_data = User_Serializer(user)
                    device = request.device
                    Login_details.objects.create(email = email,device =device,login_time=str(datetime.datetime.now())).save()
                    return JsonResponse({'status_code':'success','user':serialized_user_data.data})
                return JsonResponse({'status_code':'failed','error':'incorrect password'})
            return JsonResponse({'status_code':'failed','error':'user email id does not exist'})
        
        # handles login_type swg
        elif login_type == 'swg':
            if Users.objects.filter(email=email).exists():
                user= Users.objects.get(email=email)
                serialized_user_data = User_Serializer(user)
                Login_details.objects.create(email = email).save()
                return JsonResponse({'status_code':'success','user':serialized_user_data.data})
        
        # handles for wrong login_type
        return JsonResponse({'status_code':'failed','error':'login_type is invalid, options are swe and swg'})
    
    def get(self,request):
        #******************************************************************************#
        #    handle get request comming to endpoint login                                                            
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})            
    def put(self,request):
        #******************************************************************************#
        #   handle put request comming to endpoint login                               #
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a put request to this url'})
    def delete(self,request):
        #******************************************************************************#
        #   handle delete request comming to endpoint login                            #
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a delete request to this url'})
            
            
class SignUp(APIView):
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   display_name    :   name of the user shown in public                       #              
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #   profile_url     :   profile image url                                      #              
        #                                                                              # 
        #*******************************************************************************
        try:
            display_name        = request.data['display_name']
            email               = request.data['email']
            password            = make_password(request.data['password'],PASSWORD_ENCRYPTION_KEY)
            print(password)
            profile_url         = request.data['profile_url']
            login_type          = request.data['login_type']
        except:
            return JsonResponse({'Required fields :':'display_name, email, password, profile_url, login_type'})
        user_exist_status = Users.objects.filter(email = email).exists()
        if not user_exist_status:
            
            # creating new user
            Users.objects.create(display_name=display_name,email=email,password=password,profile_url=profile_url,login_type=login_type).save()
            
            # opening wallet for the new user
            User_Wallet.objects.create(email=email, amount = 0).save()

            return JsonResponse({'status':'user created successfully','status_code':'success'})
        else:
            return JsonResponse({"error":"user email id already exist.",'status_code':"failed"})
        
    def get(self,request):
        #******************************************************************************#
        #  handle get request comming to endpoint SignUp                                #
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})
    def put(self,request,email_id):
        #******************************************************************************#
        #   handle put request comming to endpoint SignUp                               #
        #*******************************************************************************
        if Users.objects.filter(email=email_id).exists():
            try:
                display_name    = request.data['display_name']
                profile_url     = request.data['profile_url']
            except:
                return JsonResponse({'Required fields :':'display_name, profile_url'})
            user                =  Users.objects.get(email=email_id)
            user.display_name   = display_name
            user.profile_url    = profile_url
            user.save()
            return JsonResponse({'status_code':'success','status':'user profile updated'})
        else:
            return JsonResponse({'status_code':'failed','error':'email id do not exist'})
    def delete(self,request):
        #******************************************************************************#
        #   handle delete request comming to endpoint SignUp                            #
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a delete request to this url'})
            
class Email(APIView):
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   subject            :   suject to send                                      #              
        #   message            :   message to send                                     #
        #   recipient_email    :   receiver email id                                   #
        #   template_model     :   otp or message                                      #
        #                                                                              # 
        #*******************************************************************************
        try:
            subject             = request.data['subject']
            message             = request.data['message']
            recipient_email     = request.data['recipient_email']
            template_model      = request.data['template_model']
        except:
            return JsonResponse({'Required fields : ':'subject, message, recipient_email, template_model (otp, message)'})
        try:
            
            # handle otp 
            if template_model =='otp':
                try:
                    html_content = render_to_string('mail/otp.html',{'otp':message})
                except:
                    return JsonResponse({'error':'render to string error, mail not send','status_code':'failed'})
                
            # handle message
            if template_model == 'message':
                html_content = render_to_string('mail/message.html',{'message':message})
            text_content = strip_tags(html_content)
            
            # send mail
            try:
                send_mail(
                    subject,
                    text_content,
                    EMAIL_HOST_USER,
                    [recipient_email,]
                )
                return JsonResponse({'status':'mail send successfully','status_code':'success'})
            except Exception as e:
                return JsonResponse({'error':'email error, mail not send','status_code':'failed','reason':str(e)})
     
        except Exception as e:
            print(e)
            return JsonResponse({'error':'unkown error, mail not send','status_code':'failed'})
        
    def get(self,request):
        #******************************************************************************#
        #      handle delete request comming to endpoint Email                         # 
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a post request to this url'})
    def delete(self,request):
        #******************************************************************************#
        #   handle delete request comming to endpoint Email                            #
        #*******************************************************************************
                return JsonResponse({'you are just a kid, you are not allowed to send a delete request to this url'})
            
#Endpoint to Upload File
class Donation_content(APIView):
    def get(self,request,category):
        #******************************************************************************#
        #  handle delete request comming to endpoint Donation_content                  # 
        #*******************************************************************************
        if category =='all':
            donation_content = reversed(Donations.objects.all())
        else:
            donation_content     = reversed(Donations.objects.filter(category=category))
        
        # serializing the data to send response
        serialized_content       = DonationContent_Serializer(donation_content,many = True)
        return JsonResponse({"donation_content":serialized_content.data})

    def put(self,request,id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   current_amount           :   current amount in accont                      #              
        #   heart                    :   similar to like                               #
        #                                                                              # 
        #*******************************************************************************
        try:
            current_amount = int(request.data['current_amount'])
            heart          = int(request.data['heart'])
        except:
            return JsonResponse({'Required fields :':'current_amount, heart ,(options : status ["pending","rejected","running","completed"])'})
        
        if Donations.objects.filter(id=id).exists():
            try:
                current_donation                    = Donations.objects.get(id=id)
                current_donation.current_amount     = current_amount
                current_donation.heart              = heart
                
                try:
                    status = request.data['status']
                    if status in ["pending","rejected","running","completed"]:
                        current_donation.status = status
                        if status == 'completed':
                            try:
                                completed_on         = request.data['completed_on']
                                new_donation_history = Donation_History.objects.create(media_type = current_donation.media_type,
                                                                                    target        = current_donation.target,
                                                                                    heart         = current_donation.heart,
                                                                                    title         = current_donation.title,
                                                                                    description   = current_donation.description,
                                                                                    location      = current_donation.location,
                                                                                    donation_type = current_donation.donation_type,
                                                                                    category      = current_donation.category,
                                                                                    upload_on     = current_donation.upload_on,
                                                                                    completed_on  = completed_on,
                                                                                    )
                                new_donation_history.save()
            
                            except Exception as e:
                                return JsonResponse({'status_code':'failed','Required':'completed_on','error':str(e)})
                    else:
                        return JsonResponse({'status_code':'failed','Required':'status can be ["pending","rejected","running","completed"]'})
                except:
                    pass
                current_donation.save()
                return JsonResponse(({'status_code':'success','status':'donation upated'}))
            except:
                
                return JsonResponse(({'status_code':'failed','error':'could not save, invalid data'}))
        else:
            return JsonResponse(({'status_code':'failed','error':'id does not exist'}))
        
    def delete(self,request,id):
        #******************************************************************************#
        #  handle delete request comming to endpoint Donation_content                  #
        #*******************************************************************************
        if Donations.objects.filter(id=id).exists():
            Donations.objects.filter(id=id).delete()
            return JsonResponse({'status_code':'success','status':'Donation added successfully'})
        else:
            return JsonResponse({'status_code':'failed','error':'Donation id does not exist'})
        
class Featured_content(APIView):
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   media_url           :   it should be video url (mp4)                       #              
        #   profile_image_url   :   profile image                                      #
        #   profile_username    :   username of profile                                #
        #   organisation        :   name of organisation of the content                #
        #   description         :   description about the featured                     #
        #   location            :   location of specific content                       #
        #                                                                              # 
        #*******************************************************************************
        try:
            media_url           = request.data['media_url']
            profile_image_url   = request.data['profile_image_url']
            profile_username    = request.data['profile_username']
            organisation        = request.data['organisation']
            description         = request.data['description']
            location            = request.data['location']
        except:
            return JsonResponse({'status_code':'failed','Required fields':'media_url, profile_image_url, profile_username, organisation, descripton, location'})
        
        # creating new featured content
        Featured.objects.create(media_url           =media_url,
                                profile_image_url   =profile_image_url,
                                profile_username    =profile_username,
                                organisation        =organisation,
                                description         =description,
                                location            =location).save()
        
        return JsonResponse({"status":"done",'status_code':'success'})
    def get(self,request):
        #******************************************************************************#
        #   handle delete request comming to endpoint Donation_content                 #
        #*******************************************************************************
        featured_content    = Featured.objects.all()
        serialized_content  = FeaturedContent_Serializer(featured_content,many=True)
        return JsonResponse({"featured_content":serialized_content.data,'status_code':'success'})
    def put(self,request,id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Featured.objects.filter(id=id).exists():
            try:
                featured_content    = Featured.objects.all()
                featured_content.update(running_status = False)
                this_content        = Featured.objects.get(id = id)
                this_content.running_status = True
                this_content.save()
            except:
                return Response({'status_code':'failed','error':'unknown error, could not save the changes'})
            return JsonResponse({'status':'featured content updated or changed','status_code':'success'})
        else:
            return JsonResponse({'status_code':'failed','status':'please provide a valid id'})
    def delete(self,request,id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
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
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email_id        :   email id of new user                                   #              
        #   platform        :   list of social media platform                          #
        #   media_type      :   mention login method, options are                      #
        #   category        :   provide valid donation category                        #
        #   location        :   location from where the content belongs to             #
        #   media_url       :   provide the media url in mp4 or jpg format             #
        #   title           :   title of the content                                   #
        #   description     :   description of the content                             #
        #   target          :   target amount of the donation                          # 
        #*******************************************************************************
        '''Listen to post request to the upload endpoint
        required parameter  :
        
        => VIDEO  : platform, media_type, video_url, title, description, tag
        => IMAGE  : platform, media_type, image, caption
        '''
        try:
            email_id        = request.data['email_id']
            platform        = request.data['platform']
            media_type      = str(request.data['media_type']).upper()
            category        = request.data['category']
            location        = request.data['location']
            media_url       = request.data['media_url']
            title           = request.data['title']
            description     = request.data['description']
            target          = int(request.data['target'])
            
            # validating the category
            if not Donation_categories.objects.filter(name=category).exists():
                return JsonResponse({'status_code':'failed','error':'category do not exist'})
            # validating the email id
            if not Users.objects.filter(email=email_id).exists():
                return JsonResponse({'status_code':'failed','error':'email do not exist'})
            
            profile_url         = Users.objects.get(email=email_id).profile_url
            platform_list       = platform.split(',')
        except Exception as e:
            return JsonResponse({'Required fields':'email_id,platform, media_type, category, location, media_url, title, description, target','reason':str(e)})
        
        # creating instance of social_media class
        social_media = Social_Media()
        
        # creating donatin history
        
        # handle video
        platform = []
        
        if media_type == "VIDEO":
            if 'instagram' in platform_list:
                try:
                    self.status = social_media.Upload_video_to_instagram(media_url,title)
                    if self.status:
                        platform.append('instagram')
                except Exception as e:
                    pass
            if 'facebook' in platform_list:
                try:
                    self.status = social_media.Upload_video_to_facebook(media_url,title,description)
                    if self.status:
                        platform.append('facebook')
                except Exception as e:
                   pass
            if 'youtube' in platform_list:
                try:
                    self.status = social_media.Upload_video_to_youtube(media_url,title,description,category) 
                    if self.status:
                        platform.append('youtube')
                except Exception as e:
                    pass
            if 'amarshan' in platform_list:
                    platform.append('amarshan')                
        # handle image        
        elif media_type == "IMAGE":
            if 'instagram' in platform_list:
                try:
                    self.status = social_media.Upload_image_to_instagram(image_url=media_url,caption=title)
                    if self.status:
                        platform.append('instagram')
                except Exception as e:
                        pass
            if 'facebook' in platform_list:
                try:
                    self.status = social_media.Upload_image_to_facebook(media_url,title )
                    if self.status:
                        platform.append('facebook')
                except Exception as e:
                        pass
            if 'amarshan' in platform_list: 
                try:
                    platform.append('amarshan')
                except Exception as e:
                    pass
                
        Donations.objects.create(
                media_url       = media_url,
                media_type      = media_type,
                title           = title, 
                description     = description,
                category        = category,
                location        = location,
                target          = target,
                profile_url     = profile_url,
                email_id        = email_id,
                platform        = ','.join(platform)
            ).save()
                    
        # return true if video uploaded to all platforms
        return JsonResponse({"status_code":'success','status':'Content are successfully uploaded','platform': str(','.join(platform))})
            

    def get(self,request):
        #******************************************************************************#
        #   handle delete request comming to endpoint Donation_content                                                          #
        #*******************************************************************************
        '''Listen to the get request for the endpoint upload'''
        return JsonResponse({"The method is not accessble. please try post using the fields :","For video => * video_url, * title, * description, * tag, * platform, * media type.","For Image =>* image, *caption, *platform, media_type"})
    
# Social Media access
'''---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
class Social_Media:
    
    # thread for instagram video
    def uploading_thread_method(self,video_container_id,access_token,page_id):
        #******************************************************************************#
        #    handle uploading thread of instagram                                      #
        #*******************************************************************************
        print('Startted uploading media to instagram...')
        while requests.get("https://graph.facebook.com/{}?fields=status_code&access_token={}".format(video_container_id,access_token)).json().get('status_code')!="FINISHED":
            time.sleep(1)
        print('Media uploaded to instagram successfully')
        print('Making the instagram video public accessable')
        post_url = "https://graph.facebook.com/{}/media_publish?creation_id={}&access_token={}".format(page_id,video_container_id,access_token)
        try:
            response = requests.post(post_url)
            print('post is available at instagram id : ',response.json().get('id'))
            return True
        except:
            return False
        
    '''
     uploading video
     -----------------------------------------------------------------------
    '''
    def Upload_video_to_instagram(self,video_url,title):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        '''Required parameter :
        => video_url, title
        '''
        # validating the video_url
        if video_url is None:
            return JsonResponse({"Input Error":"video url cannot be empty and it should be valid"})
        
        # collecting the neccassary data for instagram upload
        get_url         = f"https://graph.facebook.com/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
        data            = {
            "video_url":video_url,
            "caption":title,
            "access_token":ACCESS_TOKEN_FACEBOOK_PAGE,
            "media_type":"VIDEO",
        }
        
        # sending request
        print('Requesting video container id from instagram...')
        response = requests.post(get_url,json=data)
        print(response.json())
        
        # collecting video container id
        video_container_id = int(response.json().get('id'))
        
        # validating the contatiner
        if video_container_id is None:
            return JsonResponse({'status':'failed to get the container id from graph api'})
        
        print('Got container id ',video_container_id)
        
        #starting thread to upload
        threading.Thread(target=self.uploading_thread_method,
                         args=(video_container_id,
                               ACCESS_TOKEN_FACEBOOK_PAGE,
                               INSTAGRAM_BUSINESS_ACCOUNT_ID)).start()
        return True
    
    def Upload_video_to_facebook(self,video_url,title,description):
        #******************************************************************************#
        #   upload video to facebook                                                   #
        #*******************************************************************************
        url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/videos"
        
        # setting up the data to upload
        data = {
            "file_url"      :video_url,
            "title"         :title,
            "description"   :description,
            "access_token"  :ACCESS_TOKEN_FACEBOOK_PAGE,
        }
        
        # sending request
        response = requests.post(url,json=data)
        if response.json().get('id') is None:
            return False
        else:
            print('post is availble at facebook id ',response.json().get('id'))
            return True
        
    def Upload_video_to_youtube(self, video_url,title,description,tag):
        #******************************************************************************#
        #   Required Fields                                                            #
        #*******************************************************************************
        '''Required parameters
        => video_url, title, description, tag
        '''
        chuck_size = 256
        
        # downloading video from url
        downloaded_video = requests.get(video_url,stream=True)
        print('Starting to download video from the url, please wait... ',video_url,end="")
        try:
            os.remove('live_yt.mp4')
        except:
            pass
        with open('live_yt.mp4',"wb") as f:
            for chunk in downloaded_video.iter_content(chunk_size=chuck_size):
                f.write(chunk)
        print('Downloaded successfully')
        
        # uploading video to youtube
        print("Starting uploading media to youtube")
        try:
            run = f'py API/Important_file/upload_to_youtube.py  --title="{title}" --description="{description}" --keywords="{tag}"  --file="live_yt.mp4" '
            os.system(run)
            return True
        except:
            return False
    
    def Upload_video_to_amarshan(self, video_url,title,description,category,location,target,profile_url,email_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        #*******************************************************************************
        try:
            return True
        except:
            return False

    '''
    Uploading image
    ----------------------------------------------------------------
    '''
    def Upload_image_to_instagram(self,image_url,caption):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        '''
        Required parameters :
        => image_url, caption
        '''
        page_id         = INSTAGRAM_BUSINESS_ACCOUNT_ID #instagram bussiness account id
        access_token    = ACCESS_TOKEN_FACEBOOK_PAGE
        get_url         = "https://graph.facebook.com/v10.0/{}/media?image_url={}&access_token={}&caption={}".format(page_id,image_url,access_token,caption)
        print('Requesting for the image container id...')
        print('hitting on url : ',get_url)
        # print(get_url)
        response        = requests.post(get_url)
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
        post_url    = "https://graph.facebook.com/v10.0/{}/media_publish?creation_id={}&access_token={}".format(page_id,image_container_id,access_token)
        response    = requests.post(post_url)
        print('post id : ',response.json().get('id'))
        if response.json().get('id') is not None:
            return True
        else:
            return False

    def Upload_image_to_facebook(self, image_url,caption):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        '''Required parameters :
        => image_url, caption
        '''
        access_token    = ACCESS_TOKEN_FACEBOOK_PAGE
        page_id         = FACEBOOK_PAGE_ID
        response        = requests.post("https://graph.facebook.com/{}/photos?access_token={}&url={}".format(page_id,access_token, image_url))
        print(response.json())
        if response.status_code == 200:
            print('Post created successfully!')
            return True
        else:
            print('Error creating post:', response.json()['error']['message'])
            return False
        
    def Upload_image_to_amarshan(self,image_url, title, description, category,location,target,profile_url,email_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            Donations.objects.create(
                media_url   = image_url,
                media_type  = 'IMAGE',
                title       = title, 
                description = description,
                category    = category,
                location    = location,
                target      = target,
                profile_url = profile_url,
                email_id    = email_id
            ).save()
            return True
        except Exception as e:
            print('Exception',e)
            return False
        
   



class Handle_Products(APIView):
    def get(self,request,filter):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        
        if filter == 'all':
            filter_result = Products.objects.all()
        else:
            #category filtering
            filter_result = Products.objects.filter(category=filter)
            
        serialized_data = Product_Serializer(filter_result,many=True)
        return Response({'products':serialized_data.data})
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            name            = request.data['name']
            price           =request.data['price']
            description     = request.data['description']
            category        = request.data['category']
            rating          = request.data['rating']
            image_1_url     = request.data['image_1_url']
            image_2_url     = request.data['image_2_url']
            image_3_url     = request.data['image_3_url']
            image_4_url     = request.data['image_4_url']
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
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Products.objects.filter(id=filter).exists():
            try:
                name        = request.data['name']
                price       = request.data['price']
                description = request.data['description']
                category    = request.data['category']
                rating      = request.data['rating']
                image_1_url = request.data['image_1_url']
                image_2_url = request.data['image_2_url']
                image_3_url = request.data['image_3_url']
                image_4_url = request.data['image_4_url']
            except:
                return JsonResponse({'status_code':'failed','Required fields':'name, description, category, rating, image_1_url, image_2_url, image_3_url, image_4_url, price'})
        
        
            try:
                product             = Products.objects.get(id=filter)
                product.name        = name
                product.price       = price
                product.description = description
                product.category    = category 
                product.rating      = rating
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
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Products.objects.filter(id=filter).exists():
            Products.objects.get(id=filter).delete()
            return JsonResponse({'status_code':'success','status':'product deleted successfully'})
        else:
            return JsonResponse({'status_code':'failed','status':'The product id does not exists or product already deleted'})
        
class Handle_categories(APIView):
    def get(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        categories              = Categories.objects.all()
        Serialized_categories   = Category_Serializer(categories,many=True)
        return JsonResponse({'categories':Serialized_categories.data})
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            
            name            = request.data['name']
            description     = request.data['description']
            image_url       = request.data['image_url']
        except Exception as e:
            return JsonResponse({'status_code':'failed','Required Fields' : 'name, description, image_url'})
        
        if Categories.objects.filter(name=name).exists():
            return JsonResponse({'status_code':'failed','status':'category already exist'})
        new_category = Categories.objects.create(name=name,description=description)
        new_category.save()
        
        return JsonResponse({'status_code':'success','status':'category created succesfully'})
    

class Handle_Donation_categories(APIView):
    def get(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        category = Donation_categories.objects.all()
        serialized_categories = Donation_category_serializer(category,many=True)
        return JsonResponse({'status_code':'successs','categories':serialized_categories.data})
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            name = request.data['name']
            description= request.data['description']
        except:
            return JsonResponse({'status_code':'failed','Required fields':'name, description'})
        if Donation_categories.objects.filter(name = name).exists():
            return JsonResponse({'status_code':'failed', 'error':'category already exist'})
        Donation_categories.objects.create(name=name, description= description).save()
        return JsonResponse({'status_code':'success','status':'category created successfully'})
    def put(self,request,id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Donation_categories.objects.filter(id=id).exists():
            try:
                image_url           = request.data['image_url']
                catogory            = Donation_categories.objects.get(id=id)
                catogory.image_url  = image_url
                catogory.save()
                return JsonResponse({'status_code':'success','status':'catagory updated successfully'})
            except:
                return JsonResponse({"status_code":'failed','Requiried':'image_url'})
        else:
            return JsonResponse({"status_code":'failed','error':'category id do not exist'})
        
class Handle_Notifications(APIView):
    def get(self, request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        notifications               = Notification.objects.all()
        serialized_notifications    = Notification_serializer(notifications,many=True)
        return JsonResponse({'status_code':'success','notifications':serialized_notifications.data})
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
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
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
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
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Users.objects.filter(email = email_id).exists():
            user                        = Users.objects.get(email = email_id)
            user_address_serialized     = User_Address_Serializer(user)
            return JsonResponse({'address':user_address_serialized.data,'status_code':'success'})
        else:
            return JsonResponse({'status':'email id does not exist','status_code':'failed'})
    def put(self,request,email_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
            if Users.objects.filter(email = email_id).exists():
                user = Users.objects.get(email = email_id)
                try:
                    user.display_name       = request.data['display_name']
                    user.building_name      = request.data['building_name']
                    user.street_name        = request.data['street_name']
                    user.pincode            = request.data['pincode']
                    user.city               = request.data['city']
                    user.state              = request.data['state']
                    user.country            = request.data['country']
                    user.landmark           = request.data['landmark']
                    user.phone_number       = request.data['phone_number']
                    user.save()
                    return JsonResponse({'status':'address updated succesfully','status_code':'success'})
                except:
                    return JsonResponse({'Required':'display_name, building_name, street_name, landmark, pincode, city, state, country, phone_number','status_code':'failed'})
                    
        
class Handle_myorders(APIView):
    def get(self,request,email_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Users.objects.filter(email = email_id).exists():
            orders                  = Orders.objects.filter(email_id=email_id)
            user                    = Users.objects.get(email = email_id)
            user_address_serialized = User_Address_Serializer(user)
            serialized_orders       = Order_Serializer(orders,many= True)
            return JsonResponse({'status_code':'success','order_details':serialized_orders.data,'address_details':user_address_serialized.data})
        else:
            return JsonResponse({'status_code':'failed','error':' Invalide email id'})
    def post(self,request,email_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if Users.objects.filter(email = email_id).exists():
            try:   
                product_name            = request.data['product_name']
                product_description     = request.data['product_description']
                product_price           = request.data['product_price']
                product_image_url       = request.data['product_image_url']
                item_count              = request.data['item_count']
                ordered_on              = request.data['ordered_on']
            except:
                return JsonResponse({'status_code':'failed','Required fields':'product_name, product_description, product_price, product_image_url, item_count, ordered_on'})
       
            try:
                Orders.objects.create(email_id=email_id,
                                      product_name=product_name,
                                      product_description=product_description, 
                                      product_price=product_price, 
                                      product_image_url=product_image_url,
                                      item_count = item_count,
                                      ordered_on=ordered_on).save()
                return JsonResponse({'status_code':'success','orders':'order places succesfully'})
            except Exception as e:
                return JsonResponse({'status_code':'failed','error':str(e)})
        else:
            return JsonResponse({'status_code':'failed','error':' Invalide email id'})
    def put(self,request,order_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
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
    def delete(self,request,order_id):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            Orders.objects.get(id=order_id).delete()
            return JsonResponse({'status_code':'success'})
        except Exception as e:
            return JsonResponse({'status_code':'failed','error':str|(e)})
            
        
class Handle_Donation_History(APIView):
    def get(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        donations_done = Donation_History.objects.all()
        donations_done_serialized = Donation_History_Serializer(donations_done,many=True)
        return JsonResponse({'status_code':'success','history':donations_done_serialized.data})
    
class TrafficInfo(APIView):
    def get(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        login_details = reversed(Login_details.objects.all())
        serialized_login_details = Login_Detail_Serializer(login_details,many=True)
        return JsonResponse({'status_code':'success','login_details':serialized_login_details.data})
    
    
class Handle_Storage(APIView):
    def post(self,request):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        media = request.data['media']
        try:
            media.name.index(' ')
            return JsonResponse({'status_code':'failed','status':'filename cannot contain spaces'})
        except:
            pass
        Storage.objects.create(media=media).save()
        url = 'https://amarshan.s3.ap-northeast-1.amazonaws.com/media/'+media.name
        return JsonResponse({'status_code':'success','url':url})
    
class Handle_Payment(APIView):
    def get(self,request,email):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        if not Donation_Payment.objects.filter(user_email_id=email).exists():
            return JsonResponse({'status_code':'failed','error':'no payment history'})
        data = Donation_Payment.objects.filter(user_email_id = email)
        Serialized_payment = Payment_Serializer(data,many=True)
        return JsonResponse({'status_code':'success','payment':Serialized_payment.data})
    
    def post(self,request,email):
        #******************************************************************************#
        #   Required Fields                                                            #
        # --------------------                                                         #
        #   email           :   email id of new user                                   #              
        #   password        :   new password for new user                              #
        #   login_type      :   mention login method, options are                      #
        #                       ('swe' - signup with email,'swg' - signup with google) #
        #                                                                              # 
        #*******************************************************************************
        try:
            user_email_id       = email
            amount              = int(request.data["amount"])
            public_email_id     = request.data['public_email']
            donation_title      = request.data['donation_title']
            donation_id         = int(request.data['donation_id'])
        except:
            return JsonResponse({'status_code':'failed','Required':'amount, public_email, donation_title, donation_id'})

        try:
            Donation_Payment.objects.create(amount=amount,
                                            user_email_id=user_email_id,
                                            donation_title=donation_title,
                                            donation_id=donation_id,
                                            public_email_id=public_email_id).save()
            return JsonResponse({'status_code':'success'})
        except Exception as e:
            return JsonResponse({'status_code':'failed','error':str(e)})
        
class Handle_User_Wallet(APIView):
    def get(self,request,email):
        if User_Wallet.objects.filter(email = email).exists():
            wallet = User_Wallet.objects.get(email=email)
            serialized_wallet = User_Wallet_Serializer(wallet)
            return JsonResponse({'status_code':'success','wallet':serialized_wallet.data})
        else:
            return JsonResponse({'status_code':'failed','error':'wallet not found for this email, please signup. wallet is created on signup'})
    def put(self,request,email):
        if User_Wallet.objects.filter(email = email).exists():
            try:
                new_amount = request.data['amount']
            except:
                return JsonResponse({'status_code':'failed','Required':'amount'})
            try:
                wallet = User_Wallet.objects.get(email=email)
                wallet.amount = int(wallet.amount)+int(new_amount)
                wallet.save()
                return JsonResponse({'status_code':'success'})
            except Exception as e:
                return JsonResponse({'status_code':'failed','error':str(e)})
        else:
            return JsonResponse({'status_code':'failed','error':'wallet not found for this email, please signup. wallet is created on signup'})

class Handle_User_Change_Password(APIView):
    def put(self,request,email):
        if not Users.objects.filter().exists():
            return JsonResponse({'status_code':'failed','status':'email id does not exist'})
        try:
            newpassword = request.data['password']
            user = Users.objects.get(email=email)
            user.password = make_password(newpassword,PASSWORD_ENCRYPTION_KEY)
            user.save()
            return JsonResponse({'status_code':'success','status':'password changed successfully'})
        except:
            return JsonResponse({'status_code':'failed','Required':'password'})
