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
  CPDictionary _corpImageDict;
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
    _corpImageDict = [CPDictionary dictionary];
  }

  return self;
}

-(CPImage) getImageForObject:(id)obj
{
  var image = nil;
  
  if (obj.model == @"eve.character")
  {
    if ([_charImageDict containsKey:obj.pk])
    {
      image = [_charImageDict objectForKey:obj.pk];
    }
    
    else
    {
      var url = charImageURL + obj.pk + "_64" + ".jpg";

      image = [[CPImage alloc] initWithContentsOfFile:url];
      [_charImageDict setObject:image forKey:obj.pk];
    }
  }
  
  
  return image;
}

@end