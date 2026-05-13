from django.urls import path

from unlock_engine.api.views.pass_views import (
    PassListCreateAPIView,
    PassRetrieveUpdateDestroyAPIView,
    PassByCodeAPIView,
    BulkGeneratePassAPIView,
    ExportPassZipAPIView,
    ExportPassPDFAPIView
)

urlpatterns = [

    path(
        '',
        PassListCreateAPIView.as_view(),
        name='pass-list-create'
    ),

    path(
    'bulk-generate/',
        BulkGeneratePassAPIView.as_view(),
        name='bulk-generate-passes'
    ),

    path(
        'export-zip/',
        ExportPassZipAPIView.as_view(),
        name='export-pass-zip'
    ),

    path(
        'export-pdf/',
        ExportPassPDFAPIView.as_view(),
        name='export-pass-pdf'
    ),

    path(
        '<int:pk>/',
        PassRetrieveUpdateDestroyAPIView.as_view(),
        name='pass-detail'
    ),
    path(
        'by-code/<str:pass_code>/',
        PassByCodeAPIView.as_view(),
        name='pass-by-code'
    ),
    
]