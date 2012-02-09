// 
//  LoginController.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-02-02.
//  Copyright 2012 Scienceondope. All rights reserved.
// 

@import <Foundation/Foundation.j>

// ==============
// = Used URL's =
// ==============

var loginURL     = "/accounts/login/";
var logoutURL    = "/accounts/logout/";
var registerURL  = "/accounts/register/";

// =================
// = Notifications =
// =================

LoginControllerLoginSuccessful = @"LoginControllerLoginSuccessful";

// =========================
// = Class LoginController =
// =========================

@implementation LoginController : CPWindowController
{
  @outlet CPImageView   eveIconView;
  @outlet CPTextField   registerEmailTextField;
  @outlet CPTextField   registerUsernameTextField;
  @outlet CPTextField   registerPasswordTextField;
  @outlet CPTextField   registerConfirmTextField;
  @outlet CPButton      registerButton;
  
  @outlet CPTextField   loginUsernameTextField;
  @outlet CPTextField   loginPasswordTextField;
  @outlet CPButton      loginButton;
  
  @outlet CPTextField   messageTextField;
  
  CPImage               _eveIcon;
  CPURLConnection       _registerConnection;
  CPURLConnection       _loginConnection;
}

-(void)awakeFromCib
{
  _eveIcon = [[CPImage alloc] initWithContentsOfFile:"./Resources/eve.png"];
  [eveIconView setImage:_eveIcon];
}

-(@action) login:(id)sender
{
  var bundle = [CPBundle mainBundle];
  
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var GET  = "?username=" + [loginUsernameTextField stringValue];
      GET += "&password=" + [loginPasswordTextField stringValue];
  
  var request = [CPURLRequest requestWithURL:baseURL + loginURL + GET];
  _loginConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(@action) register:(id)sender
{
  var bundle = [CPBundle mainBundle];
  
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var GET  = "?email="    + [registerEmailTextField stringValue];
      GET += "&username=" + [registerUsernameTextField stringValue];
      GET += "&password=" + [registerPasswordTextField stringValue];
      GET += "&confirm="  + [registerConfirmTextField stringValue];
      
  var request = [CPURLRequest requestWithURL:baseURL + registerURL + GET];
  _registerConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(void)connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  var result = CPJSObjectCreateWithJSON(data);
  
  console.log(result);
  
  if (connection == _loginConnection)
  {
    [messageTextField setStringValue:result.message];
    
    if (result.success)
    {
      window.setTimeout(function() { 
          [[CPNotificationCenter defaultCenter] postNotificationName:LoginControllerLoginSuccessful object:self];
        }, 500);
    }
  }
  
  if (connection == _registerConnection)
  {
    [messageTextField setStringValue:result.message];
  }
}

-(void)connection:(CPURLConnection)connection didFailWithError:(CPError)error
{
  console.log(error);
}
@end