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

eveAddAPIKeyURL         = "/eve/addAPIKey/"
eveRemoveAPIKeyURL      = "/eve/removeAPIKey/"
eveAPIKeyURL            = "/eve/apiKeys/"

eveCharactersURL        = "/eve/characters/"
eveCorporationsURL      = "/eve/corporations/"

eveMarketGroupTreeURL   = "/evedb/invMarketGroupTree/"