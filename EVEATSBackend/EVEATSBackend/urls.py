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
    url(r'^assets/marketGroups/$', 'assets.views.marketGroups'),
    url(r'^assets/marketGroups/(?P<id>\d+)/$', 'assets.views.marketGroups'),
    url(r'^assets/listEveIcons/$', 'assets.views.listEveIcons'),
    url(r'^assets/listEveIcons/(?P<id>\d+)/$', 'assets.views.listEveIcons'),
    url(r'^assets/listCorpAssets/$', 'assets.views.listCorpAssets'),
    url(r'^assets/listCorpAssets/(?P<groupID>\d+)/$', 'assets.views.listCorpAssets'),
    url(r'^assets/getTreeForTypeID/(?P<ID>\d+)/$', 'assets.views.getTreeForTypeID'),
    url(r'^assets/listCorpAssetsByName/$', 'assets.views.listCorpAssetsByName'),

    # accounts app
    url(r'^accounts/register/$', 'accounts.views.register'),
    url(r'^accounts/verifyEmailAddress/$', 'accounts.manage.verifyEmailAddress'),
    url(r'^accounts/requestPassword/$', 'accounts.manage.verifyEmailAddress'),
    url(r'^accounts/listAccounts/$', 'accounts.views.listAccounts'),
    url(r'^accounts/login/$', 'accounts.views.login'),
    url(r'^accounts/logout/$', 'accounts.views.logout'),
    url(r'^accounts/info/$', 'accounts.views.info'),

    # eve app
    url(r'^eve/addAPIKey/$', 'eve.views.addAPIKey'),
    url(r'^eve/removeAPIKey/$', 'eve.views.removeAPIKey'),
    url(r'^eve/apiKeys/$', 'eve.views.apiKeys'),
    url(r'^eve/characters/$', 'eve.views.characters'),
    url(r'^eve/corporations/$', 'eve.views.corporations'),
    url(r'^eve/characterAssetsByMarketGroup/(?P<charID>\d+)/$', 'eve.views.characterAssetsByMarketGroup'),
    url(r'^eve/characterAssetsByMarketGroup/(?P<charID>\d+)/(?P<marketGroupID>\d+)$', 'eve.views.characterAssetsByMarketGroup'),
    url(r'^eve/characterAssetsByTypeName/(?P<charID>\d+)/(?P<typeName>[\w\ ]+)$', 'eve.views.characterAssetsByTypeName'),
    url(r'^eve/characterAssetsDetailTree/(?P<charID>\d+)/(?P<typeID>\d+)/(?P<locationID>\d+)/$', 'eve.views.characterAssetsDetailTree'),
    
    # evedb app
    url(r'^evedb/invType/(?P<typeID>\d+)/$', 'evedb.views.invType'),
    url(r'^evedb/invMarketGroup/(?P<marketGroupID>\d+)/$', 'evedb.views.invMarketGroup'),
    url(r'^evedb/invMarketGroupTree/$', 'evedb.views.invMarketGroupTree'),
    
    # common app
    url(r'^common/authentificationError/$', 'common.views.authentificationError'),
    url(r'^common/permissionError/$', 'common.views.permissionError'),
    url(r'^common/exeptionRaised/$', 'common.views.exeptionRaised'),
    url(r'^common/httpPostTest/$', 'common.views.httpPostTest'),
    
    # djcelery
    url(r'^tasks/', include('djcelery.urls')),
)

urlpatterns += staticfiles_urlpatterns()