from django.contrib import admin
from .models import UserProfile, Event,  Guest, RSVP, Vendor, Category,CoverImage, BirthdayParty, Wedding, InaugurationEvent
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
        ('Personal Info', {'fields': ('full_name', 'phone')}),
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
    list_display = ('id','category_name',)
    list_filter = ('category_name',)
    search_fields = ('category_name',)
    ordering = ('category_name',)

@admin.register(CoverImage)
class CoverImageAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id','image',)
    list_filter = ('image',)
    search_fields = ('image',)
    ordering = ('image',)



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'event_type', 'date', 'start_time', 'end_time', 'venue', 'is_published')
    list_filter = ('event_type', 'date', 'is_published')
    search_fields = ['title', 'description', 'venue']
    date_hierarchy = 'date'
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BirthdayParty)
class BirthdayPartyAdmin(EventAdmin):
    list_display = EventAdmin.list_display + ('celebrant_name', 'age', 'theme', 'max_guests')
    fieldsets = (
        (None, {
            'fields': ('event_type', 'title', 'description', 'date', 'start_time', 'end_time', 'venue', 'is_published')
        }),
        ('Additional Information', {
            'fields': ('celebrant_name', 'age', 'theme', 'RSVP_email', 'max_guests','gift_registry_link', 'dress_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Wedding)
class WeddingAdmin(EventAdmin):
    list_display = EventAdmin.list_display + ('bride_name', 'groom_name', 'wedding_date', 'rsvp_deadline')
    fieldsets = (
        (None, {
            'fields': ('event_type', 'title', 'description', 'date', 'start_time', 'end_time', 'venue', 'is_published')
        }),
        ('Wedding Information', {
            'fields': ('bride_name', 'groom_name', 'wedding_date', 'RSVP_email',  'max_guests', 'rsvp_deadline', 'wedding_registry_link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(InaugurationEvent)
class InaugurationEventAdmin(EventAdmin):
    list_display = EventAdmin.list_display + ('guest_of_honor', 'inauguration_date', 'venue_address')
    fieldsets = (
        (None, {
            'fields': ('event_type', 'title', 'description', 'date', 'start_time', 'end_time', 'venue', 'is_published')
        }),
        ('Inauguration Information', {
            'fields': ('guest_of_honor', 'organizer_name', 'organizer_contact', 'max_guests',  'inauguration_date', 'venue_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
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

