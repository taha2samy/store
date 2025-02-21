from purchases.models import Category,SubElement
from django.shortcuts import render
def main(request, *args, **kwargs):
    catagory =Category.objects.all()
    return render(request, 'html/just.html')