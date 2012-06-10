// 
//  BackendURLS.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-25.
//  Copyright 2012 scienceondope.org  All rights reserved.
// 

@import <Foundation/Foundation.j>

// ==================================================================================
// = base URL                                                                       =
// ==================================================================================

bundle  = [CPBundle mainBundle];
baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];

// =================================================================================
// = Backend URL's                                                                 =
// =================================================================================

userInfoURL                   = "/accounts/info/";

eveAddAPIKeyURL               = "/eve/addAPIKey/";
eveRemoveAPIKeyURL            = "/eve/removeAPIKey/";
eveAPIKeyURL                  = "/eve/apiKeys/";

eveCharactersURL              = "/eve/characters/";
eveCorporationsURL            = "/eve/corporations/";

eveCharacterAssetsByGroup     = "/eve/characterAssetsByMarketGroup/";
eveCharacterAssetsByName      = "/eve/characterAssetsByTypeName/";
eveCharacterAssetsDetailTree  = "/eve/characterAssetsDetailTree/";

eveCorporationAssetsByGroup     = "/eve/corporationAssetsByMarketGroup/";
eveCorporationAssetsByName      = "/eve/corporationAssetsByTypeName/";
eveCorporationAssetsDetailTree  = "/eve/corporationAssetsDetailTree/";

eveMarketGroupTreeURL         = "/evedb/invMarketGroupTree/";