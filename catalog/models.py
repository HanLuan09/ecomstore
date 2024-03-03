from djongo import models
from django.urls import reverse
from decimal import Decimal

class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCategoryManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):

    objects = models.Manager()
    active = ActiveCategoryManager()

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
        help_text='Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords" ,max_length=255,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog_category', args=[str(self.slug)])


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)

class Product(models.Model):
    objects = models.Manager()
    active = ActiveProductManager()


    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
        help_text='Unique value for product page URL, created from name.')
    author = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,
        blank=True,default=0.00)
    image = models.ImageField(upload_to='images/products/main') 
    thumbnail = models.ImageField(upload_to='images/products/thumbnails') 
    image_caption = models.CharField(max_length=200) 
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(max_length=255,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255,
        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ArrayReferenceField(to=Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog_product', args=[str(self.slug)])

    def sale_price(self):
        old_price_float = float(self.old_price.to_decimal())
        price_float = float(self.price.to_decimal())

        if old_price_float > price_float:
            return price_float
        else:
            return None
        
        

    


    

