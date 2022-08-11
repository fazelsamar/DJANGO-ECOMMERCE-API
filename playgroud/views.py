from django.shortcuts import render
from store.models import Product
def hello(r):
    q = Product.objects.select_related('collection').all()
    for i in q:
        i.collection.id
    context = {}
    return render(r, 'playground/index.html', context)