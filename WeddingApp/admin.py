from django.contrib import admin
from .models import UserProfile, Event, BirthdayParty, WeddingCard, Guest, RSVP, Vendor, Category,CoverImage
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

@admin.register(BirthdayParty)
class BirthdayPartyAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'start_time', 'end_time', 'venue', 'is_published', 'created_at', 'updated_at', 'celebrant_name', 'age', 'theme', 'guest_of_honor')
    list_filter = ('date', 'is_published')
    search_fields = ('description', 'venue', 'celebrant_name', 'theme', 'guest_of_honor')

@admin.register(WeddingCard)
class WeddingCardAdmin(admin.ModelAdmin):
    list_display = ('description', 'date', 'start_time', 'end_time', 'venue', 'is_published', 'created_at', 'updated_at', 'bride_name', 'groom_name', 'wedding_date', 'RSVP_email')
    list_filter = ('date', 'is_published')
    search_fields = ('description', 'venue', 'bride_name', 'groom_name')

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

