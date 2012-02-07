// 
//  ImageCache.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-02-06.
//  Copyright 2012 Scienceondope All rights reserved.
// 

@import <Foundation/Foundation.j>

// =========
// = URL's =
// =========

var charImageURL = "http://image.eveonline.com/Character/";

// =============
// = Singleton =
// =============

IMGCache = nil;

// ====================
// = Class ImageCache =
// ====================

@implementation ImageCache : CPObject
{
  CPDictionary _charImageDict;
}

+(ImageCache)sharedCache
{
  if(!IMGCache)
  {
    IMGCache = [[ImageCache alloc] init];
  }
  
  return IMGCache;
}

-(id) init
{
  self = [super init];
  
  IMGCache = self;
  
  if (self)
  {
    _charImageDict = [CPDictionary dictionary];
  }

  return self;
}

-(CPImage) getCharImageForID:(CPString)id
{
  var image = nil;
  
  if ([_charImageDict containsKey:id])
  {
    image = [_charImageDict objectForKey:id];
  }
  
  else 
  {
    var url = charImageURL + id + "_64" + ".jpg";
    
    image = [[CPImage alloc] initWithContentsOfFile:url];
    [_charImageDict setObject:image forKey:id];
  }
  
  return image;
}

@end