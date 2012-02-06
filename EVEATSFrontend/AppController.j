/*
 * AppController.j
 * testApp
 *
 * Created by You on February 1, 2012.
 * Copyright 2012, Your Company All rights reserved.
 */

@import <Foundation/CPObject.j>
@import "LoginController.j"


@implementation AppController : CPObject
{
    @outlet CPWindow    theWindow; //this "outlet" is connected automatically by the Cib
    @outlet CPPanel     loginPanel;
}

- (void)applicationDidFinishLaunching:(CPNotification)aNotification
{
    // This is called when the application is done loading.
    
    [[CPNotificationCenter defaultCenter] 
      addObserver:self
      selector:@selector(loginSuccessfulNotificationPosted:)
      name:LoginControllerLoginSuccessful
      object:nil];

}

- (void)awakeFromCib
{
  console.log("AppConntroller");
  
    // This is called when the cib is done loading.
    // You can implement this method on any object instantiated from a Cib.
    // It's a useful hook for setting up current UI values, and other things.

    // In this case, we want the window from Cib to become our full browser window
    [theWindow setFullPlatformWindow:YES];
}

-(void) loginSuccessfulNotificationPosted:(id)sender
{
  //[loginPanel close];
  [[[sender object] loginPanel] close];
  [theWindow orderFront:self];
}
@end
