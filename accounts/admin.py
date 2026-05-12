# Import Django admin module
# Used to register models so they appear
# inside Django admin panel.
from django.contrib import admin


# UserAdmin:
# Django's built-in admin configuration
# specifically designed for user/auth models.
#
# Provides:
# - password hashing support
# - secure password change form
# - permission handling
# - group handling
# - authentication-related admin features
# - makes password fields read-only
#
# Better than normal ModelAdmin
# for custom user models.
from django.contrib.auth.admin import UserAdmin


# Import custom user model
from .models import Account


# =====================================================
# CUSTOM ADMIN CONFIGURATION
# =====================================================
# Controls:
# - list page
# - edit page
# - filters
# - field organization
# - admin behavior
# =====================================================
class AccountAdmin(UserAdmin):

    # -------------------------------------------------
    # Columns shown in admin list page
    #
    # Example:
    # Email | Username | Active | Staff
    #
    # Can also include:
    # - custom methods
    # - model properties
    # - callable functions
    # -------------------------------------------------
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'last_login',
        'is_active',
        'is_staff',
        'date_joined'
    )

    # -------------------------------------------------
    # Adds right-side filter sidebar
    #
    # Example:
    # filter by:
    # - active users
    # - staff users
    # - joined date
    #
    # Common usage:
    #
    # list_filter = (
    #     'is_staff',
    #     'is_active',
    # )
    # Empty means no filters shown.
    # -------------------------------------------------
    list_filter = ()

    # -------------------------------------------------
    # Used for ManyToMany fields.
    #
    # Creates dual selection UI.
    #
    # Commonly used for:
    # - groups
    # - user_permissions
    #
    # Example:
    #
    # filter_horizontal = (
    #     'groups',
    #     'user_permissions',
    # )
    # Empty because no ManyToMany
    # fields are configured currently.
    # -------------------------------------------------
    filter_horizontal = ()

    # -------------------------------------------------
    # Organizes fields into sections
    # on admin edit page.
    #
    # Allows:
    # - grouping fields
    # - custom layouts
    # - collapsible sections
    #
    # Example:
    #
    # fieldsets = (
    #     ('Personal Info', {
    #         'fields': (
    #             'first_name',
    #             'last_name'
    #         )
    #     }),
    # )
    #
    # Empty means Django uses
    # default UserAdmin layout.
    # -------------------------------------------------
    fieldsets = ()

    # -------------------------------------------------
    # Other commonly used options:
    #
    # search_fields
    # -> adds search bar
    #
    # ordering
    # -> default sorting
    #
    # readonly_fields
    # -> non-editable fields
    #
    # Example:
    #
    # search_fields = ('email', 'username')
    #
    # ordering = ('-date_joined',)
    #
    # readonly_fields = (
    #     'last_login',
    # )
    # -------------------------------------------------
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    # Makes selected columns clickable
    #
    # Clicking these fields opens
    # the user edit/details page.
    #
    # Without this:
    # Django automatically makes
    # first column clickable.
    #
    # Useful when:
    # - multiple important identifiers exist
    # - easier navigation needed
    # - admin usability improvement
    #
    # Example:
    # clicking email or username
    # opens user edit page.
    #
    # Can include:
    # - model fields
    # - fields from list_display
    #
    # NOTE:
    # fields used here must also
    # exist inside list_display.
    # -------------------------------------------------
    list_display_links = (
        'email','username',
    )
        
# =====================================================
# REGISTER MODEL IN ADMIN PANEL
# =====================================================
# Connects:
#
# Account model
# +
# AccountAdmin configuration
#
# Without this:
# model won't appear in admin panel.
# =====================================================
admin.site.register(Account, AccountAdmin)

