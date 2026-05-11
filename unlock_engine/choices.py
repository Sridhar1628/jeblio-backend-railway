from django.db import models


class CampaignType(models.TextChoices):
    TREASURE_HUNT = "TREASURE_HUNT", "Treasure Hunt"
    WORKSHOP = "WORKSHOP", "Workshop"
    INTERNSHIP = "INTERNSHIP", "Internship"
    PLACEMENT = "PLACEMENT", "Placement"
    INFLUENCER = "INFLUENCER", "Influencer"
    COLLEGE_DRIVE = "COLLEGE_DRIVE", "College Drive"


class CampaignStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    PAUSED = "PAUSED", "Paused"
    COMPLETED = "COMPLETED", "Completed"
    EXPIRED = "EXPIRED", "Expired"


class RewardType(models.TextChoices):
    SCHOLARSHIP = "SCHOLARSHIP", "Scholarship"
    WORKSHOP = "WORKSHOP", "Workshop"
    MENTORSHIP = "MENTORSHIP", "Mentorship"
    CONSULTATION = "CONSULTATION", "Consultation"
    INTERNSHIP = "INTERNSHIP", "Internship"
    COURSE_ACCESS = "COURSE_ACCESS", "Course Access"


class RewardRarity(models.TextChoices):
    COMMON = "COMMON", "Common"
    RARE = "RARE", "Rare"
    EPIC = "EPIC", "Epic"
    LEGENDARY = "LEGENDARY", "Legendary"


class PassStatus(models.TextChoices):
    GENERATED = "GENERATED", "Generated"
    DISTRIBUTED = "DISTRIBUTED", "Distributed"
    SCANNED = "SCANNED", "Scanned"
    CLAIMED = "CLAIMED", "Claimed"
    CONVERTED = "CONVERTED", "Converted"
    EXPIRED = "EXPIRED", "Expired"
    BLOCKED = "BLOCKED", "Blocked"


class ConsultationStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    ASSIGNED = "ASSIGNED", "Assigned"
    SCHEDULED = "SCHEDULED", "Scheduled"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CONVERTED = "CONVERTED", "Converted"
    DROPPED = "DROPPED", "Dropped"


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    INITIATED = "INITIATED", "Initiated"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    REFUNDED = "REFUNDED", "Refunded"
    CANCELLED = "CANCELLED", "Cancelled"