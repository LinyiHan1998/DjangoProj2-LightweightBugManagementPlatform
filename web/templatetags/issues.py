from django.template import Library
from web import models
from django.urls import reverse

register = Library()

@register.simple_tag
def string_just(nums):
    if nums < 100:
        nums=str(nums).rjust(3,"0")
    return "#{}".format(nums)