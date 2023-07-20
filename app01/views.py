import boto3
from django.shortcuts import render,HttpResponse
from app01.utils.aws.awsSNS import SnsWrapper
from django.conf import settings
# Create your views here.

def send_sms(request):
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION_NAME
    )
    sns_wrapper = SnsWrapper(session.resource("sns"))
    topic = sns_wrapper.sns_resource.create_topic(Name="RequirementTacer")
    # topic_name = "RequirementTacer"

    email_send = sns_wrapper.publish_message(topic, 'love me', {"key": 'bytes'})
    print(email_send)
    session = boto3.Session(
        aws_access_key_id="AKIAWPX26A2EXIBI5QHU",
        aws_secret_access_key="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",
        region_name="us-west-1"
    )

    return HttpResponse('Success')

