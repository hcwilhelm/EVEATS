from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EVEATS.views.home', name='home'),
    # url(r'^EVEATS/', include('EVEATS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # ==========================================
    # = MarketGroup hierarchy as Json response =
    # ==========================================
    (r'^assets/marketGroups/$', 'assets.views.marketGroups'),
    (r'^assets/marketGroups/(?P<id>\d+)/$', 'assets.views.marketGroups'),
    (r'^assets/listEveIcons/$', 'assets.views.listEveIcons'),
    (r'^assets/listEveIcons/(?P<id>\d+)/$', 'assets.views.listEveIcons'),
    (r'^assets/listCorpAssets/$', 'assets.views.listCorpAssets'),
    (r'^assets/listCorpAssets/(?P<groupID>\d+)/$', 'assets.views.listCorpAssets'),
    (r'^assets/getTreeForTypeID/(?P<ID>\d+)/$', 'assets.views.getTreeForTypeID'),
    (r'^assets/listCorpAssetsByName/$', 'assets.views.listCorpAssetsByName'),

    # accounts app
    (r'^accounts/register/$', 'accounts.views.register'),
    (r'^accounts/verifyEmailAddress/$', 'accounts.manage.verifyEmailAddress'),
    (r'^accounts/requestPassword/$', 'accounts.manage.verifyEmailAddress'),
    (r'^accounts/listAccounts/$', 'accounts.views.listAccounts'),
    (r'^accounts/login/$', 'accounts.views.login'),
    (r'^accounts/logout/$', 'accounts.views.logout'),
    (r'^accounts/info/$', 'accounts.views.info'),

    # eveapi app
    (r'^eveapi/addApiKey/$', 'eveapi.views.addApiKey'),
    (r'^eveapi/listApiKeys/$', 'eveapi.views.listApiKeys'),

)

urlpatterns += staticfiles_urlpatterns()