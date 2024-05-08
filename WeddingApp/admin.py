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
    list_display = ('category_name',)
    list_filter = ('category_name',)
    search_fields = ('category_name',)
    ordering = ('category_name',)

@admin.register(CoverImage)
class CoverImageAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('id','image','event_type')
    list_filter = ('image','event_type')
    search_fields = ('image','event_type')
    ordering = ('image','event_type')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_type',  'event_start_time', 'event_end_time', 'venue_address', 'is_published')
    list_filter = ('event_type', 'event_date', 'is_published')
    search_fields = ['title', 'description', 'venue_address']
    date_hierarchy = 'event_date'
    ordering = ('event_date',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BirthdayParty)
class BirthdayPartyAdmin(EventAdmin):
    list_display = EventAdmin.list_display + ('celebrant_name', 'age', 'theme', 'max_guests')
    fieldsets = (
        (None, {
            'fields': ('title', 'event_type', 'description')
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_start_time', 'event_end_time', 'venue_address', 'venue_pin_code', 'is_published', 'max_guests', 'theme')
        }),
        ('Additional Information', {
            'fields': ('celebrant_name', 'age', 'gift_registry_link', 'dress_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Wedding)
class WeddingAdmin(EventAdmin):
    list_display = EventAdmin.list_display + ('bride_name', 'groom_name', 'event_date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'event_type', 'description')
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_start_time', 'event_end_time', 'venue_address', 'venue_pin_code', 'is_published')
        }),
        ('Wedding Information', {
            'fields': ('bride_name', 'groom_name', 'bride_mother_name', 'bride_father_name', 'groom_mother_name', 'groom_father_name', 'wedding_registry_link', 'max_guests')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(InaugurationEvent)
class InaugurationEventAdmin(EventAdmin):
    list_display = EventAdmin.list_display + ('guest_of_honor','organizer_name','organizer_contact',)
    fieldsets = (
        (None, {
            'fields': ('title', 'event_type', 'description')
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_start_time', 'event_end_time', 'venue_address', 'venue_pin_code', 'is_published')
        }),
        ('Inauguration Information', {
            'fields': ('guest_of_honor', 'organizer_name', 'organizer_contact',  'max_guests')
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

