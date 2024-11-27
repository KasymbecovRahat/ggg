from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description', )


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'store_description', 'address', )


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', )


@register(ProductCombo)
class ProductComboTranslationOptions(TranslationOptions):
    fields = ('combo_name', 'combo_description' )