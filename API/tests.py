from facebookads.adobjects.adimage import AdImage

image = AdImage(parent_id='act_653009763501606')
image[AdImage.Field.filename] = 'img.jpg'
image.remote_create()

# Output image Hash
print(image[AdImage.Field.hash])