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
var corpImageURL = "http://image.eveonline.com/Corporation/";
var typeImageURL = "http://image.eveonline.com/Type/";

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
  CPDictionary _typeImageDict;
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
    _typeImageDict = [CPDictionary dictionary];
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
      var url = charImageURL + obj.pk + "_64.jpg";

      image = [[CPImage alloc] initWithContentsOfFile:url];
      [_charImageDict setObject:image forKey:obj.pk];
    }
  }
  
  if (obj.model == @"eve.corporation")
  {
    if ([_corpImageDict containsKey:obj.pk])
    {
      image = [_corpImageDict objectForKey:obj.pk];
    }
    
    else
    {
      var url = corpImageURL + obj.pk + "_64.png";
      
      image = [[CPImage alloc] initWithContentsOfFile:url];
      [_corpImageDict setObject:image forKey:obj.pk];
    }
  }
  
  
  return image;
}

-(CPImage) getImageForTypeID:(int)typeID
{
  var image = nil;
  
  if ([_typeImageDict containsKey:typeID])
  {
    image = [_typeImageDict objectForKey:typeID];
  }
  
  else
  {
    var url = typeImageURL + typeID + "_64.png"
    
    image = [[CPImage alloc] initWithContentsOfFile:url];
    [_typeImageDict setObject:image forKey:typeID];
  }
  
  return image;
}
@end