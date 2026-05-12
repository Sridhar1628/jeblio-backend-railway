from django.urls import include, path

urlpatterns = [
    path(
        'campaigns/',
        include('unlock_engine.api.urls.campaign_urls')
    ),

    path(
        'rewards/',
        include('unlock_engine.api.urls.reward_urls')
    ),

    path(
        'passes/',
        include('unlock_engine.api.urls.pass_urls')
    ),

    path(
        'leads/',
        include('unlock_engine.api.urls.lead_urls')
    ),
]