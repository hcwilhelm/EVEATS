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

ImageCache = [[ImageCache alloc] init];

// ====================
// = Class ImageCache =
// ====================

@implementation ImageCache : CPObject
{
  CPDictionary _charImageDict;
}

-(id) init
{
  self = [super init];
  
  _charImageDict = [CPDictionary dictionary];
  
  return self;
}

-(CPImage) getImageForID:(CPString)id
{
  var image = nil;
  
  if [_charImageDict containsKey:id]
  {
    image = [_charImageDict objectForKey:id];
  }
  
  else 
  {
    var url = charImageURL + "id" + "_64";
    image = [[CPImage alloc] initWithContentsOfFile:url];
    
    [_charImageDict setObject:image forKey:id];
  }
  
  return image;
}

@end