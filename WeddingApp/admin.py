from django.contrib import admin
from .models import UserProfile, Event,  Guest, RSVP, Vendor, Category,CoverImage,ContactUs
from django.contrib.auth.admin import UserAdmin

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ( 'id','full_name', 'email',  'phone', 'is_staff', 'is_active','is_superuser')
    search_fields = ('email', 'full_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('email',) 

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone','image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name','category_image')
    list_filter = ('category_name','additional_fields','category_image')
    search_fields = ('category_name','additional_fields','category_image')
    ordering = ('category_name',)

@admin.register(CoverImage)
class CoverImageAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id','image','event_category')
    list_filter = ('image','event_category')
    search_fields = ('image','event_category')
    ordering = ('image','event_category')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','user', 'event_category', 'event_date', 'event_start_time', 'event_end_time', 'is_published')
    list_filter = ('event_category', 'is_published', 'event_date')
    search_fields = ('title', 'description', 'venue_name', 'venue_address')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('event_category','user','title', 'description')
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_start_time', 'event_end_time', 'venue_name', 'venue_address', 'venue_pin_code')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number', 'organizer_name', 'guest_of_honor')
        }),
        ('Additional Information', {
            'fields': ('max_guests', 'theme', 'dress_code', 'gift_sending_link', 'is_published','is_seen')
        }),
        ('Wedding Specific', {
            'fields': ('bride_name', 'groom_name', 'bride_mother_name', 'bride_father_name', 'groom_mother_name', 'groom_father_name', 'bride_age', 'groom_age'),
            'classes': ('collapse',)
        }),
        ('Birthday Specific', {
            'fields': ('birthday_person_name', 'birthday_person_age'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'is_attending')
    list_filter = ('event', 'is_attending')
    search_fields = ('name', 'email')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'guest', 'response')
    list_filter = ('event', 'response')
    search_fields = ('guest__name',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'event')
    list_filter = ('event',)
    search_fields = ('name', 'service')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('id','name', 'email','message')
    list_filter = ('name',)
    search_fields = ('name', 'email','message')
    ordering = ('name',)
