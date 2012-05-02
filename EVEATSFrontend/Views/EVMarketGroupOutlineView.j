// 
//  EVMarketGroupOutlineView.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-27.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 


@import <Foundation/Foundation.j>
@import <AppKit/CPOutlineView.j>

@import "EVMarketGroupDataView.j"

@implementation EVMarketGroupOutlineView: CPOutlineView
{
  
}

-(id) initWithFrame:(CPRect)aFrame
{
  self = [super initWithFrame:aFrame];
  
  if (self)
  {
    var marketGroupColumn = [[CPTableColumn alloc] initWithIdentifier:"marketGroupColumn"];
    
    var dataView = [[EVMarketGroupDataView alloc] initWithFrame:CPRectMake(0,0,200, 20)];
    [marketGroupColumn setDataView: dataView];
    
    [self setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
    [self setHeaderView:nil];
    [self setCornerView:nil];
    [self setColumnAutoresizingStyle:CPTableViewLastColumnOnlyAutoresizingStyle];
    [self addTableColumn:marketGroupColumn];
    [self setOutlineTableColumn:marketGroupColumn];
    [self setTarget:self];
  }
  
  return self
}

@end