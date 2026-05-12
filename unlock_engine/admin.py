from django.contrib import admin

from unlock_engine.models.campaign_models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'campaign_code',
        'campaign_type',
        'status',
        'total_passes',
        'total_claims',
        'total_conversions',
        'is_active',
        'created_at',
    ]

    list_filter = [
        'campaign_type',
        'status',
        'is_active',
        'created_at',
    ]

    search_fields = [
        'name',
        'campaign_code',
        'influencer_name',
        'region',
    ]

    readonly_fields = [
        'uuid',
        'slug',
        'created_at',
        'updated_at',
        'total_scans',
        'total_claims',
        'total_conversions',
    ]

    ordering = ['-created_at']

from unlock_engine.models.reward_models import Reward


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'reward_name',
        'reward_code',
        'campaign',
        'reward_type',
        'rarity',
        'remaining_quantity',
        'claimed_quantity',
        'status',
        'is_active',
        'created_at',
    ]

    list_filter = [
        'reward_type',
        'rarity',
        'status',
        'is_active',
        'created_at',
    ]

    search_fields = [
        'reward_name',
        'reward_code',
        'campaign__name',
    ]

    readonly_fields = [
        'uuid',
        'created_at',
        'updated_at',
        'claimed_quantity',
        'total_views',
        'total_claims',
        'total_conversions',
    ]

    ordering = ['-created_at']

from unlock_engine.models.pass_models import Pass


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'pass_code',
        'campaign',
        'status',
        'scan_count',
        'is_claimed',
        'distribution_source',
        'distribution_region',
        'is_active',
        'created_at',
    ]

    list_filter = [
        'status',
        'distribution_source',
        'distribution_region',
        'is_claimed',
        'is_active',
        'created_at',
    ]

    search_fields = [
        'pass_code',
        'serial_number',
        'campaign__name',
        'distribution_college',
    ]

    readonly_fields = [
        'uuid',
        'scan_count',
        'first_scanned_at',
        'claimed_at',
        'converted_at',
        'created_at',
        'updated_at',
    ]

    ordering = ['-created_at']

from unlock_engine.models.claim_models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'full_name',
        'email',
        'phone_number',
        'campaign',
        'assigned_reward',
        'funnel_stage',
        'is_otp_verified',
        'reward_claimed',
        'payment_completed',
        'created_at',
    ]

    list_filter = [
        'funnel_stage',
        'is_otp_verified',
        'reward_claimed',
        'payment_completed',
        'is_active',
        'created_at',
    ]

    search_fields = [
        'full_name',
        'email',
        'phone_number',
        'campaign__name',
        'college_name',
    ]

    readonly_fields = [
        'uuid',
        'otp_verified_at',
        'reward_claimed_at',
        'converted_at',
        'created_at',
        'updated_at',
    ]

    ordering = ['-created_at']