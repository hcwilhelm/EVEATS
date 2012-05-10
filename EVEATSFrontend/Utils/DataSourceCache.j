// 
//  DataSourceCache.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-25.
//  Copyright 2012 Scienceondope.org All rights reserved.
// 


@import <Foundation/Foundation.j>

// =============
// = Singleton =
// =============

DSCache = nil;

@implementation DataSourceCache : CPObject
{
  CPDictionary _apiKeys @accessors(property=apiKeys);
  CPDictionary _characters @accessors(property=characters);
  CPDictionary _corporations @accessors(property=corporations);
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

@end
