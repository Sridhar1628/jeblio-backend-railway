from django.utils import timezone


def track_pass_scan(qr_pass):

    qr_pass.scan_count += 1

    if not qr_pass.first_scanned_at:
        qr_pass.first_scanned_at = timezone.now()

    qr_pass.save()

    campaign = qr_pass.campaign

    campaign.total_scans += 1
    campaign.save()