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

var userInfoURL     = "/accounts/info/";
var apiKeysURL      = "/eveapi/apiKeys/";
var addAPIKeyURL    = "/eveapi/addAPIKey/";
var removeAPIKeyURL = "/eveapi/removeAPIKey/"; 


// =================
// = Notifications =
// =================

UserControllerAPIKeyChanged = @"UserControllerAPIKeyChanged";

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
  
  @outlet CPPopover     addAPIKeyPopover;
  @outlet CPTextField   keyIDTextField;
  @outlet CPTextField   vCodeTextField;
  @outlet CPTextField   nameTextField;
  @outlet CPButton      addApiKeyButton;
  @outlet CPButton      cancelButton;
  
  CPButton              _plusButton;
  CPButton              _minusButton;
  
  CPURLConnection       _userInfoConnection;
  CPURLConnection       _apiKeyConnection;
  CPURLConnection       _addAPIKeyConnection;
  CPURLConnection       _removeAPIKeyConnection;
  
  CPObject              _apiKeys;
}

-(void)awakeFromCib
{
  console.log("awakeformCIB");
  
  // ===================
  // = apiKeyTableView =
  // ===================
  
  var idColumn = [[CPTableColumn alloc] initWithIdentifier:"keyID"];
  [[idColumn headerView] setStringValue:"Key ID"];
  [idColumn setMinWidth:100];
  
  var vcodeColumn = [[CPTableColumn alloc] initWithIdentifier:"vCode"];
  [[vcodeColumn headerView] setStringValue:"Verification Code"];
  [vcodeColumn setWidth:400];
  
  var nameColumn = [[CPTableColumn alloc] initWithIdentifier:"name"];
  [[nameColumn headerView] setStringValue:"Name"];
  [nameColumn setWidth:100];
  
  var validColumn = [[CPTableColumn alloc] initWithIdentifier:"isValid"];
  [[validColumn headerView] setStringValue:"Valid"];
  [validColumn setWidth:50];
  
  [apiKeyTableView addTableColumn:idColumn];
  [apiKeyTableView addTableColumn:vcodeColumn];
  [apiKeyTableView addTableColumn:nameColumn];
  [apiKeyTableView addTableColumn:validColumn];
  
  [apiKeyTableView setDataSource:self];
  
  // =============
  // = buttonBar =
  // =============
  
  _plusButton   = [CPButtonBar plusButton];
  _minusButton  = [CPButtonBar minusButton];
  
  [_plusButton setTarget:self];
  [_plusButton setAction:@selector(addKeyPopover:)];
  
  [_minusButton setTarget:self];
  [_minusButton setAction:@selector(removeKey:)];
  
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

-(@action) addKeyPopover:(id)sender
{
  [addAPIKeyPopover close];
  [addAPIKeyPopover showRelativeToRect:nil ofView:sender preferredEdge:nil];
}

-(@action) removeKey:(id)sender
{
  console.log([apiKeyTableView selectedRow]);
  
  if ([apiKeyTableView selectedRow] > -1)
  {
    var bundle = [CPBundle mainBundle];
    var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];

    var GET  = "?keyID="  + _apiKeys[[apiKeyTableView selectedRow]]['pk'];
    
    var request = [CPURLRequest requestWithURL:baseURL + removeAPIKeyURL + GET];
    _removeAPIKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  }
}

-(@action) addKey:(id)sender
{
  var bundle = [CPBundle mainBundle];
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var GET  = "?keyID="  + [keyIDTextField stringValue];
      GET += "&vCode="  + [vCodeTextField stringValue];
      GET += "&name="   + [nameTextField stringValue];

  var request = [CPURLRequest requestWithURL:baseURL + addAPIKeyURL + GET];
  _addAPIKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];

  [addAPIKeyPopover close];
}

-(@action) closeWindow:(id)sender
{
  [addAPIKeyPopover close];
}

-(void) connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  var result = CPJSObjectCreateWithJSON(data);
  
  if (connection == _userInfoConnection)
  {
    [usernameTextField setStringValue:result[0].fields.username];
    [emailTextField setStringValue:result[0].fields.email];
  }
  
  if (connection == _apiKeyConnection)
  {
    _apiKeys = result;
    [apiKeyTableView reloadData];
    
    [[CPNotificationCenter defaultCenter] postNotificationName:UserControllerAPIKeyChanged object:self];
  }
  
  if (connection == _addAPIKeyConnection)
  {
    if (result["success"] == YES)
    {
      _apiKeys = nil;
      [apiKeyTableView reloadData];
    }
  }
  
  if (connection == _removeAPIKeyConnection)
  { 
    if (result["success"] == YES)
    {
      _apiKeys = nil;
      [apiKeyTableView reloadData];
    }
    
  }
}

-(int) numberOfRowsInTableView:(CPTableView)aTableView
{
  if (_apiKeys == nil)
  {
    var bundle = [CPBundle mainBundle];
    var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
    
    var request = [CPURLRequest requestWithURL:baseURL + apiKeysURL];
    _apiKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];
    
    return 0;
  }
  
  else
  {
    return _apiKeys.length;
  }
}

-(id) tableView:(CPTableView)aTableView objectValueForTableColumn:(CPTableColumn)aTableColumn row:(int)rowIndex
{
    if ([aTableColumn identifier] == "keyID")
    {
      return _apiKeys[rowIndex].fields['keyID'];
    }
    
    if ([aTableColumn identifier] == "vCode")
    {
      return _apiKeys[rowIndex].fields['vCode'];
    }
    
    if ([aTableColumn identifier] == "name")
    {
      return _apiKeys[rowIndex].fields['name'];
    }
    
    if ([aTableColumn identifier] == "isValid")
    {
      return _apiKeys[rowIndex].fields['valid'];
    }
}

@end
