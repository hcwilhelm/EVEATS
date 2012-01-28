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
	
	
)

urlpatterns += staticfiles_urlpatterns()