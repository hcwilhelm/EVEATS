// 
//  EVTableColumnIconView.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-05-03.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 

@import <Foundation/Foundation.j>

@import "../Utils/ImageCache.j"

@implementation EVTableColumnIconView: CPView
{
  CPImageView     _iconView            @accessors(property=groupIcon);
}

-(id) initWithFrame:(CPRect)aFrame
{
  self = [super initWithFrame:aFrame];
  
  if (self)
  {
    _iconView = [[CPImageView alloc] initWithFrame:aFrame];
    
    [self addSubview: _iconView];
  }
  
  return self;
}

-(void) setObjectValue:(int)typeID
{ 
  var imageCache = [ImageCache sharedCache];
  [_iconView setImage:[imageCache getImageForTypeID:typeID]];
}

-(id) initWithCoder:(CPCoder)aCoder
{
    self = [super initWithCoder:aCoder];

    if (self)
    {
      _iconView = [aCoder decodeObjectForKey:@"_iconView"];
    }

    return self;
}

-(void) encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:_iconView forKey:@"_iconView"];
}

@end