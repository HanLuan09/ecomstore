from search.models import SearchTerm
from catalog.models import Product
from django.db.models import Q

STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
               'of', 'on', 'or', 'that', 'the', 'to', 'with']

# Store the search text in the database
def store(request, q):
    # If the search term is at least three chars long, store in the database
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        term.save()
    # return

# Get products matching the search text
def products(search_text):
    words = _prepare_words(search_text)
    products = Product.active.all().results = Product.objects.filter(name__icontains=search_text) 

    results = {'products': []}

    # Iterate through keywords
    for word in words:
        products = products.filter(
            Q(name__icontains=word) |
            Q(description__icontains=word) |
            Q(sku__iexact=word) |
            Q(meta_description__icontains=word) |
            Q(meta_keywords__icontains=word)
        )

    results['products'] = products

    return results

# Strip out common words, limit to 5 words
def _prepare_words(search_text):
    words = search_text.split()
    words = [word.lower() for word in words]  # Convert to lowercase
    words = [word for word in words if word not in STRIP_WORDS]
    return words[:5]  # Limit to 5 words
