

import boto3
import datetime



today = datetime.datetime.today()
today = today.strftime("%Y%m%d")

def lambda_handler(event, context):

    s3_api = boto3.client('s3')

    bucket_name = "my-data-file-for-sorting"
    response = s3_api.list_objects_v2(Bucket=bucket_name)
    Contents = response.get('Contents')
    
    file_folder_in_bucket = [ filename['Key'] for filename in Contents]

    directory = today + '/'

    if directory not in file_folder_in_bucket:
        s3_api.put_object(Bucket=bucket_name, Key=directory)


    for item in Contents:
        creation_date = item.get('LastModified').strftime("%Y%m%d")
        item_name = item.get('Key')

        if creation_date == today and '/' not in item_name:
            s3_api.copy_object(Bucket=bucket_name, CopySource=bucket_name+"/"+item_name, Key=directory+item_name)
            s3_api.delete_object(Bucket=bucket_name, Key=item_name)



