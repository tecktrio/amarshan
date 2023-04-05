import boto3
client = boto3.client('s3',aws_access_key_id="AKIA4VO2ARB3GD7FP2KM",aws_secret_access_key="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")
file_path = "API\yt2.mp4"
bucket_name = "tecktrio-portfolio"
# upload = client.upload_file(file_path, bucket_name, "file_name")
url = client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key':"2023-03-04 10-19-46.mp4"})
print(url)