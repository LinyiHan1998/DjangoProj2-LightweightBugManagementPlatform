import uuid
import os
import base64
from io import BytesIO
from boto3.session import Session
from django.conf import settings

class AwsS3():
    def __init__(self):
        session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.REGION_NAME)
        self.s3 = session.resource("s3")
        self.client = session.client('s3')

    def upload_single_photo(self,upload_data,upload_key,bucket_name):
        try:
            res = self.client.put_object(Bucket=bucket_name,Key=upload_key, Body=upload_data)
            print(res)
            res = self.client.put_object_acl(Bucket=bucket_name, Key=upload_key, ACL='public-read')
            print(res)

        except Exception as e:
            print(e)
        # photo_stream = BytesIO(bytes(upload_data))
        #
        # self.client.upload_fileobj(photo_stream,bucket_name,upload_key)
        # with open(upload_data, 'rb') as f:
        #     photo_stream = f.read()
        #
        #     try:
        #         self.s3.Bucket(bucket_name).put_object(Key=upload_key, Body=photo_stream)
        #         print(1)
        #     except Exception as e:
        #         print(e)
    def my_create_bucket(self,bucket_name):
        bucket = self.s3.Bucket(bucket_name.lower())

        try:
            bucket.create( CreateBucketConfiguration ={ 'LocationConstraint':settings.REGION_NAME})
            print(f"Created bucket {bucket_name}.")
        except Exception as e:
            print("Create Bucket {} error:{}".format(bucket_name,e))


# if __name__ == '__main__':
#     create_bucket("/Users/linyi/Desktop/1211687485001_.pic.jpg","test.jpg")
# def usage_demo():
#     print('-'*88)
#     print("Welcome to the Amazon S3 bucket demo!")
#     print('-'*88)
#
#     logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
#     session = boto3.Session(
#         aws_access_key_id="",
#         aws_secret_access_key="",
#         region_name=""
#     )
#     s3_resource = session.resource('s3')
#     s3_resource.put('/Users/linyi/Desktop/1211687485001_.pic.jpg ')
#     prefix = 'doc-example-bucket-'
#     created_buckets = [
#         BucketWrapper(s3_resource.Bucket(prefix + str(uuid.uuid1()))) for _ in range(3)]
#     for bucket in created_buckets:
#         bucket.create()
#         print(f"Created bucket {bucket.name}.")
#
#     bucket_to_delete = created_buckets.pop()
#     if bucket_to_delete.exists():
#         print(f"Bucket exists: {bucket_to_delete.name}.")
#     bucket_to_delete.delete()
#     print(f"Deleted bucket {bucket_to_delete.name}.")
#     if not bucket_to_delete.exists():
#         print(f"Bucket no longer exists: {bucket_to_delete.name}.")
#
#     buckets = [b for b in BucketWrapper.list(s3_resource) if b.name.startswith(prefix)]
#     for bucket in buckets:
#         print(f"Got bucket {bucket.name}.")
#
#     bucket = created_buckets[0]
#     bucket.grant_log_delivery_access()
#     #acl = bucket.get_acl()
#     #print(f"Bucket {bucket.name} has ACL grants: {acl.grants}.")
#
#     put_rules = [{
#         'AllowedOrigins': ['http://www.example.com'],
#         'AllowedMethods': ['PUT', 'POST', 'DELETE'],
#         'AllowedHeaders': ['*']
#     }]
#     bucket.put_cors(put_rules)
#     get_rules = bucket.get_cors()
#     print(f"Bucket {bucket.name} has CORS rules: {json.dumps(get_rules.cors_rules)}.")
#     bucket.delete_cors()
#
#     put_policy_desc = {
#         'Version': '2012-10-17',
#         'Id': str(uuid.uuid1()),
#         'Statement': [{
#             'Effect': 'Allow',
#             'Principal': {'AWS': 'arn:aws:iam::111122223333:user/Martha'},
#             'Action': [
#                 's3:GetObject',
#                 's3:ListBucket'
#             ],
#             'Resource': [
#                 f'arn:aws:s3:::{bucket.name}/*',
#                 f'arn:aws:s3:::{bucket.name}'
#             ]
#         }]
#     }
#     try:
#         bucket.put_policy(put_policy_desc)
#         policy = bucket.get_policy()
#         print(f"Bucket {bucket.name} has policy {json.dumps(policy)}.")
#         bucket.delete_policy()
#     except ClientError as error:
#         if error.response['Error']['Code'] == 'MalformedPolicy':
#             print('*'*88)
#             print("This demo couldn't set the bucket policy because the principal user\n"
#                   "specified in the demo policy does not exist. For this request to\n"
#                   "succeed, you must replace the user ARN with an existing AWS user.")
#             print('*' * 88)
#         else:
#             raise
#
#     put_rules = [{
#         'ID': str(uuid.uuid1()),
#         'Filter': {
#             'And': {
#                 'Prefix': 'monsters/',
#                 'Tags': [{'Key': 'type', 'Value': 'zombie'}]
#             }
#         },
#         'Status': 'Enabled',
#         'Expiration': {'Days': 28}
#     }]
#     bucket.put_lifecycle_configuration(put_rules)
#     get_rules = bucket.get_lifecycle_configuration()
#     print(f"Bucket {bucket.name} has lifecycle configuration {json.dumps(get_rules)}.")
#     bucket.delete_lifecycle_configuration()
#
#     for bucket in created_buckets:
#         bucket.delete()
#         print(f"Deleted bucket {bucket.name}.")
#
#     print('Thanks for watching!')
#     print('-'*88)
# snippet-end:[python.example_code.s3.Scenario_BucketManagement]


