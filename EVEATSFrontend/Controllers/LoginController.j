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

// =======================================================
// = CSRF Cookie needed for django's XSite Protectection =
// =======================================================

var csrfCookie = [[CPCookie alloc] initWithName:@"csrftoken"];

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
  
  @outlet CPButton      postTestButton;
  
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
  var bundle  = [CPBundle mainBundle];
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var username = [loginUsernameTextField stringValue];
  var password = [loginPasswordTextField stringValue];

  var content = [[CPString alloc] initWithFormat:@"username=%@&password=%@", username, password];

  var request = [CPURLRequest requestWithURL:baseURL + loginURL]
  [request setHTTPMethod:@"POST"]; 
  [request setHTTPBody:content]; 
  [request setValue:"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
  [request setValue:[csrfCookie value] forHTTPHeaderField:@"X-CSRFToken"];

  _loginConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(@action) register:(id)sender
{
  var bundle  = [CPBundle mainBundle];
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var email     = [registerEmailTextField stringValue];
  var username  = [registerUsernameTextField stringValue];
  var password  = [registerPasswordTextField stringValue];
  var confirm   = [registerConfirmTextField stringValue];
  
  var content = [[CPString alloc] initWithFormat:@"email=%@&username%@&password=%@&confirm=%@", email, username, password, confirm];

  var request = [CPURLRequest requestWithURL:baseURL + registerURL]
  [request setHTTPMethod:@"POST"]; 
  [request setHTTPBody:content]; 
  [request setValue:"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
  [request setValue:[csrfCookie value] forHTTPHeaderField:@"X-CSRFToken"];
  
  _registerConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(@action) sendPOST:(id)sender
{
  console.log("send POST");
  
  var bundle = [CPBundle mainBundle];
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var p1 = @"Hello";
  var p2 = @"World";

  var content = [[CPString alloc] initWithFormat:@"p1=%@&p2=%@", p1, p2];

  var request = [[CPURLRequest alloc] initWithURL:baseURL + "/common/httpPostTest/"]; 
  [request setHTTPMethod:@"POST"]; 
  [request setHTTPBody:content]; 
  [request setValue:"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];

  var cookie1 = [[CPCookie alloc] initWithName:@"csrftoken"];
  [request setValue:[cookie1 value] forHTTPHeaderField:@"X-CSRFToken"];
  
  var connection = [CPURLConnection connectionWithRequest:request delegate:self];
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