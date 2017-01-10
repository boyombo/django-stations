from django.contrib import admin


from tax.models import BusinessType, Business, Payment


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_id',
                    'business_kind', 'location', 'licence_no']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['business', 'payment_id',
                    'amount', 'date_of_payment', 'expiration_date']
