from django.db import models

# class Category(models.Model):
#     title= models.CharField(max_length=50)
#     parent_category_id= models.CharField(max_length=50)

#     @staticmethod
#     def get_all_categories():
#         return Category.objects.all()

    # def __str__(self):
    #     return self.name


class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.CharField(max_length=60, default='')
    subcategory = models.CharField(max_length=60, default='')
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    #image= models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_category(category):
        if category:
            return Products.objects.filter (category=category)
        else:
            return Products.get_all_products();

    @staticmethod
    def get_all_products_by_category(subcategory):
        if subcategory:
            return Products.objects.filter (subcategory=subcategory)
        else:
            return Products.get_all_products();