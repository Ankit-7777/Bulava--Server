from django.contrib import admin
from .models import UserProfile, Event,  Guest, RSVP, Vendor, Category,CoverImage,ContactUs,Device, AppConfig, SubEvent, BannerImage, UserEvent, Group
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
    list_display = ('id','event_id', 'event_category', 'user', 'is_published','is_seen', 'created_at', 'updated_at')
    list_filter = ('event_category', 'user', 'is_published', 'is_seen')
    search_fields = ('event_category__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('event_category','event_id', 'user','cover_image_id','image', 'additional_fields', 'is_published','invited', 'is_seen')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(SubEvent)
class SubEventCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category','name','image')
    list_filter = ('name','additional_fields','image')
    search_fields = ('category','event','name','additional_fields','image')
    ordering = ('name',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_id', 'type', 'token', 'created_at', 'updated_at')
    search_fields = ('device_id', 'user__username', 'type')
    list_filter = ('type', 'created_at')
    ordering = ('-created_at',)

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

admin.site.register(AppConfig)
admin.site.register(BannerImage)
admin.site.register(UserEvent)
admin.site.register(Group)