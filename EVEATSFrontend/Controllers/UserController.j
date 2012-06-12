// 
//  UserController.j
//  testApp
//  
//  Created by Hans Christian Wilhelm on 2012-02-01.
//  Copyright 2012 Scienceondope.org All rights reserved.
// 


@import <Foundation/Foundation.j>

@import "../Utils/BackendURLS.j"
@import "../Categories/CPString_phpjs.j"


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
  [vcodeColumn setWidth:600];
  
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
  if ([apiKeyTableView selectedRow] > -1)
  {
    var key = [[[DataSourceCache sharedCache] apiKeys] objectForKey: [apiKeyTableView selectedRow]];
    
    var content = [[CPString alloc] initWithFormat:@"keyID=%d", [key objectForKey:@"pk"]];
    
    var request = [CPURLRequest requestWithURL:baseURL + eveRemoveAPIKeyURL];
    [request setHTTPMethod:@"POST"];
    [request setHTTPBody:content];
    [request setValue:"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"]; 
    [request setValue:[[[CPCookie alloc] initWithName:@"csrftoken"] value] forHTTPHeaderField:@"X-CSRFToken"];
    
    _removeAPIKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  }
}

-(@action) addKey:(id)sender
{
  var keyID   = [keyIDTextField stringValue];
  var vCode   = [vCodeTextField stringValue];
  var name    = [nameTextField stringValue];
  
  var content = [[CPString alloc] initWithFormat:@"keyID=%@&vCode=%@&name=%@", keyID, vCode, name];

  var request = [CPURLRequest requestWithURL:baseURL + eveAddAPIKeyURL];
  [request setHTTPMethod:@"POST"];
  [request setHTTPBody:content];
  [request setValue:"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"]; 
  [request setValue:[[[CPCookie alloc] initWithName:@"csrftoken"] value] forHTTPHeaderField:@"X-CSRFToken"];
  
  console.log(request);
  
  _addAPIKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  [addAPIKeyPopover close];
}

-(@action) closeWindow:(id)sender
{
  [addAPIKeyPopover close];
}

// =============================
// = CPURLConnection delegate  =
// =============================

-(void) connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  
  var json = CPJSObjectCreateWithJSON(data);
  
  if (connection == _userInfoConnection)
  {
    [usernameTextField setStringValue:json[0].fields.username];
    [emailTextField setStringValue:json[0].fields.email];
  }
  
  if (connection == _apiKeyConnection)
  {
    [[DataSourceCache sharedCache] setApiKeys: [CPDictionary dictionaryWithJSObject: json.result recursively:YES]];
    
    [apiKeyTableView reloadData];
    [[CPNotificationCenter defaultCenter] postNotificationName:UserControllerAPIKeyChanged object:self];
  }
  
  if (connection == _addAPIKeyConnection)
  {
    if (json["success"] == YES)
    {
      var request = [CPURLRequest requestWithURL:baseURL + eveAPIKeyURL];
      _apiKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];
    }
  }
  
  if (connection == _removeAPIKeyConnection)
  { 
    if (json["success"] == YES)
    {
      var request = [CPURLRequest requestWithURL:baseURL + eveAPIKeyURL];
      _apiKeyConnection = [CPURLConnection connectionWithRequest:request delegate:self];
    }
    
  }
}

// =========================
// = CPTableView delegates =
// =========================

-(int) numberOfRowsInTableView:(CPTableView)aTableView
{
  return [[[DataSourceCache sharedCache] apiKeys] count];
}

-(id) tableView:(CPTableView)aTableView objectValueForTableColumn:(CPTableColumn)aTableColumn row:(int)rowIndex
{
    var apiKeys = [[DataSourceCache sharedCache] apiKeys];
  
    if ([aTableColumn identifier] == "keyID")
    {
      return [[[apiKeys objectForKey:rowIndex] objectForKey:@"fields"] objectForKey:@"keyID"];
    }
    
    if ([aTableColumn identifier] == "vCode")
    {
      return [[[apiKeys objectForKey:rowIndex] objectForKey:@"fields"] objectForKey:@"vCode"];
    }
    
    if ([aTableColumn identifier] == "name")
    {
      return [[[apiKeys objectForKey:rowIndex] objectForKey:@"fields"] objectForKey:@"name"];
    }
    
    if ([aTableColumn identifier] == "isValid")
    {
      return [[[apiKeys objectForKey:rowIndex] objectForKey:@"fields"] objectForKey:@"valid"];
    }
}

@end
