// 
//  EVMarketGroupDataView.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-27.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 

@import <Foundation/Foundation.j>

@implementation EVMarketGroupDataView: CPView
{
  CPImageView     _groupIcon;
  CPTextField     _groupName;
  
  int             _groupID;
  String          _groupDescription;
}

-(id) initWithFrame:(CPRect)aFrame
{
  self = [super initWithFrame:aFrame];
  
  if (self)
  {
    _groupIcon = [[CPImageView alloc] initWithFrame:CGRectMake(0,0,16,16)];
    _groupName = [[CPTextField alloc] initWithFrame:CGRectMake(20,0,300,20)]; // Rect Values needs to be adjusted
    
    [self addSubview: _groupIcon];
    [self addSubview: _groupName];
  }
  
  return self;
}

-(void) setObjectValue:(id)obj
{
  console.log(obj);
  
  if (!obj)
  {
    return;
  }
  
  if ([obj objectForKey:@"iconID"] != nil)
  {
    var icon = [[CPImage alloc] initWithContentsOfFile:"./Resources/EveIcons/iconID_" + [obj objectForKey:@"iconID"] + "_grey.jpg"];
    [_groupIcon setImage:icon]
  }
  
  [_groupName setStringValue:[obj objectForKey:@"marketGroupName"]];
}

-(id) initWithCoder:(CPCoder)aCoder
{
    self = [super initWithCoder:aCoder];

    if (self)
    {
      _groupIcon          = [aCoder decodeObjectForKey:@"_groupIcon"];
      _groupName          = [aCoder decodeObjectForKey:@"_groupName"];
      _groupID            = [aCoder decodeObjectForKey:@"_groupID"];
      _groupDescription   = [aCoder decodeObjectForKey:@"_groupDescription"];
    }

    return self;
}

-(void) encodeWithCoder:(CPCoder)aCoder
{
    [super encodeWithCoder:aCoder];

    [aCoder encodeObject:_groupIcon         forKey:@"_groupIcon"];
    [aCoder encodeObject:_groupName         forKey:@"_groupName"];
    [aCoder encodeObject:_groupID           forKey:@"_groupID"];
    [aCoder encodeObject:_groupDescription  forKey:@"_groupDescription"];
}

@end