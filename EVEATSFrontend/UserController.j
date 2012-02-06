// 
//  UserController.j
//  testApp
//  
//  Created by Hans Christian Wilhelm on 2012-02-01.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 


@import <Foundation/Foundation.j>

@implementation UserController : CPObject
{
  // =======================
  // = Login Panel outlets =
  // =======================
  
  @outlet CPPanel       loginPanel;
  @outlet CPImageView   loginLogoImageView;
  @outlet CPTextField   loginUserTextField;
  @outlet CPTextField   loginPasswordTextField;
  @outlet CPButton      loginButton;
  @outlet CPButton      loginRegisterButton;
  @outlet CPTextField   loginMessageTextField;
  
  // ==========================
  // = Register Panel outlets =
  // ==========================
  
  @outlet CPPanel       registerPanel;
  @outlet CPImageView   registerLogoImageView;
  @outlet CPTextField   registerUserTextField;
  @outlet CPTextField   registerPasswordTextField;
  @outlet CPTextField   registerEmailTextField;
  @outlet CPButton      registerButton;
  @outlet CPButton      registerLoginButton;
  @outlet CPTextField   registerMessageTextField;
  
  CPImage               _eveIcon;
  CPURLConnection       _loginConnection;
  CPURLConnection       _registerConnection;
}

-(void)awakeFromCib
{
  [loginPanel setMovable:NO];
  [loginPanel center];
  
  [registerPanel setMovable:NO];
  [registerPanel center];

  _eveIcon = [[CPImage alloc] initWithContentsOfFile:"./Resources/eve.png"];
  [loginLogoImageView setImage: _eveIcon];
  [registerLogoImageView setImage: _eveIcon];
}

-(@action)loginPanelLogin:(id)sender
{
  var url = "http://www.scienceondope.org:8000/accounts/login/";
  url += "?" + "username=" + [loginUserTextField stringValue];
  url += "&" + "password=" + [loginPasswordTextField stringValue];
  
  var request = [CPURLRequest requestWithURL:url];
  _loginConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(@action)loginPanelRegister:(id)sender
{
  [loginPanel orderOut:self];
  [registerPanel orderFront:self];
}

-(@action)registerPanelRegister:(id)sender
{
  var url = "http://www.scienceondope.org:8000/accounts/registerAccount/";
  url += "?" + "username=" + [registerUserTextField stringValue];
  url += "&" + "password=" + [registerPasswordTextField stringValue];
  url += "&" + "email=" + [registerEmailTextField stringValue];
  
  var request = [CPURLRequest requestWithURL:url];
  _registerConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(@action)registerPanelLogin:(id)sender
{
  [registerPanel orderOut:self];
  [loginPanel orderFront:self];
}

-(void)connection:(CPURLConnection)connection didReceiveData:(CPString) data
{
  var result = CPJSObjectCreateWithJSON(data);
  
  if (connection == _loginConnection)
  {
    if(!result.Success)
    {
      [loginMessageTextField setStringValue: result.Message];
    }
  }
  
  if (connection == _registerConnection)
  {
    [registerMessageTextField setStringValue: result.Message];
  }
  
}

@end
