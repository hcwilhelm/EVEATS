// 
//  EVMenuItem.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-26.
//  Copyright 2012 scienceondope.org All rights reserved.
// 

@import <Foundation/Foundation.j>
@import <AppKit/CPMenuItem.j>


//
// MenuItem with model object (Character / Corporation)
//

@implementation EVMenuItem : CPMenuItem
{
  id  modelObject @accessors;
}
