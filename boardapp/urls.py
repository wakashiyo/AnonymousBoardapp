from django.contrib import admin 
from django.urls import include, path
from . import settings
from django.conf import settings
from django.urls import re_path
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comments.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    # path('sicial-auth/', include('allauth.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), # staticファイルを配信するための設定
]