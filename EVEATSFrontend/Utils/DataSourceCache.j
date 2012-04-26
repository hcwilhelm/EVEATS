// 
//  DataSourceCache.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-25.
//  Copyright 2012 Scienceondope.org All rights reserved.
// 


@import <Foundation/Foundation.j>

// =========
// = URL's =
// =========

var apiKeysURL = "/eve/apiKeys/";

// =============
// = Singleton =
// =============

DSCache = nil;

// ====================
// = Class ImageCache =
// ====================

@implementation DataSourceCache : CPObject
{
  CPArray _apiKeys @accessors(property=apiKeys);
  CPArray _characters @accessors(property=characters);
  CPArray _corporations @accessors(property=corporations);
}

+(DataSourceCache)sharedCache
{
  if(!DSCache)
  {
    DSCache = [[DataSourceCache alloc] init];
  }
  
  return DSCache;
}

-(id) init
{
  self = [super init];
  
  DSCache = self;
  
  if (self)
  {
  }

  return self;
}


