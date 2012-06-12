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
// and a ProgressView is a long running import task was started
//

@implementation EVMenuItem : CPMenuItem
{
  id      modelObject @accessors;
}

@end