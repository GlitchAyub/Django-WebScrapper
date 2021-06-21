import requests
from requests.compat import quote_plus #when you put space in every word u type it will plus %20 in the urls
from django.shortcuts import render
from bs4 import BeautifulSoup
from .import models

BASE_CRAIGSLIST_URL='https://kolkata.craigslist.org/d/services/search/bbb?query={}'
BASE_IMG_URL='https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features='html.parser')

    post_listings=soup.find_all('li',{'class':'result-row'})

    final_posting=[]

    for post in post_listings:
        post_title=post.find(class_='result-title').text
        post_url=post.find('a').get('href')
        post_image_id=post.find(class_='result-image').get('data-ids')
        if post.find(class_='result-price'):
            post_price=post.find(class_='result-price').text
        else:    
            post_price="N/A"
            
        
        # code for image display
        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url=BASE_IMG_URL.format(post_image_id)
            print( post_image_url)
        else:
            post_image_url:'https://picsum.photos/200'

        final_posting.append((post_title,post_url,post_price,post_image_url))    


    
    frontend={
        "search":search,
        "final_posting":final_posting

    }
    return render(request,'myApp/new_search.html',frontend)