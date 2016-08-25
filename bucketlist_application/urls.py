import django
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from buppli import api
from buppli.views import (BucketListView, IndexView, PublicBucketListView,
                          logout_view)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_nested.routers import NestedSimpleRouter

router = DefaultRouter()
router.register(r'auth/register', api.UserViewSet)
router.register(r'bucketlists', api.BucketListViewSet)
router.register(r'public-bucketlist', api.PublicBucketListViewSet,
                base_name='public_bucketlist')
bucketlist_router = NestedSimpleRouter(router, r'bucketlists',
                                       lookup='bucketlist')
bucketlist_router.register(r'items', api.BucketListItemViewSet)

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^bucketlists$', BucketListView.as_view()),
    url(r'^public-bucketlist$', PublicBucketListView.as_view()),
    url(r'^logout$', logout_view),
    url(r'^api/v1/login/$', obtain_jwt_token, name='login'),
    url(r'^api/v1/login/refresh_token/$', refresh_jwt_token),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(bucketlist_router.urls)),
    url(r'^api/v1/docs/', include("rest_framework_swagger.urls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$',
        django.views.static.serve, {'document_root': settings.STATIC_ROOT}),
]
