// 
//  UserController.j
//  testApp
//  
//  Created by Hans Christian Wilhelm on 2012-02-01.
//  Copyright 2012 Scienceondope.org All rights reserved.
// 


@import <Foundation/Foundation.j>

// ==============
// = Used URL's =
// ==============

var userInfoURL  = "/accounts/info/";


// ========================
// = class UserController =
// ========================

@implementation UserController : CPViewController
{
  @outlet CPTextField   usernameTextField;
  @outlet CPTextField   emailTextField;
  @outlet CPTextField   passwordTextField;
  @outlet CPTextField   confirmTextField;
  @outlet CPTableView   apiKeyTableView;
  @outlet CPButtonBar   buttonBar;
  
  CPButton              _plusButton;
  CPButton              _minusButton;
  CPURLConnection       _userInfoConnection;
}

-(void)awakeFromCib
{
  
  // ===================
  // = apiKeyTableView =
  // ===================
  
  var idColumn = [[CPTableColumn alloc] initWithIdentifier:"ID"];
  [[idColumn headerView] setStringValue:"ID"];
  [idColumn setMinWidth:100];
  
  var vcodeColumn = [[CPTableColumn alloc] initWithIdentifier:"VCode"];
  [[vcodeColumn headerView] setStringValue:"Verification Code"];
  [vcodeColumn setMinWidth:100];
  
  [apiKeyTableView addTableColumn:idColumn];
  [apiKeyTableView addTableColumn:vcodeColumn];
  
  // =============
  // = buttonBar =
  // =============
  
  _plusButton   = [CPButtonBar plusButton];
  _minusButton  = [CPButtonBar minusButton];
  
  var buttons = [CPArray array];
  [buttons addObject:_plusButton];
  [buttons addObject:_minusButton];
  
  [buttonBar setButtons:buttons]; 
  
  // ===================
  // = Query user info =
  // ===================
  
  var bundle = [CPBundle mainBundle];
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
   
  var request = [CPURLRequest requestWithURL:baseURL + userInfoURL];
  _userInfoConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(void)connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  var result = CPJSObjectCreateWithJSON(data);
  
  if (connection == _userInfoConnection)
  {
    [usernameTextField setStringValue:result[0].fields.username];
    [emailTextField setStringValue:result[0].fields.email];
  }
}
-(@action) saveClicked:(id)sender
{
  
}

@end
