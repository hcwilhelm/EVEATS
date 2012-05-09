/*
 * AppController.j
 * testApp
 *
 * Created by You on February 1, 2012.
 * Copyright 2012, Your Company All rights reserved.
 */

@import <Foundation/CPObject.j>

@import "Views/EVMenuItem.j"

@import "Controllers/LoginController.j"
@import "Controllers/UserController.j"
@import "Controllers/AssetsController.j"

@import "Utils/BackendURLS.j"
@import "Utils/ImageCache.j"
@import "Utils/DataSourceCache.j"


// ================
// = Global var's =
// ================

EVSelectedCharacter = nil;

// ===========================
// = Toolbar item identifier =
// ===========================

var CharImagePlaceholderToolbarItem = "CharImagePlaceholderToolbarItem";
var CharSelectorToolbarItem         = "CharSelectorToolbarItem";
var ManageAccountToolbarItem        = "ManageAccountToolbarItem";
var AssetsToolbarItem               = "AssetsToolbarItem";

// =======================
// = Class AppController =
// =======================

@implementation AppController : CPObject
{
    @outlet CPWindow      theWindow;
    
    //
    // The plan is to always have only one Subview !
    // Dunno if this is smart ! 
    // 
    
    CPView                _mainView
    CPView                _mainSubview

    CPToolbar             _toolbar;
    CPImageView           _charImageView;
    
    CPWindowController    _loginController;
    CPViewController      _userController;
    CPViewController      _assetsController;
    
    CPURLConnection       _apiKeyConnection;
    CPURLConnection       _charactersConnection;
    CPURLConnection       _corporationsConnection;
    
    CPObject              _characters;
}

- (void)applicationDidFinishLaunching:(CPNotification)aNotification
{
    // This is called when the application is done loading.
    
    [[CPNotificationCenter defaultCenter] 
      addObserver:self
      selector:@selector(loginSuccessfulNotificationPosted:)
      name:LoginControllerLoginSuccessful
      object:nil];
      
    [[CPNotificationCenter defaultCenter] 
      addObserver:self
      selector:@selector(APIKeyChangedNotificationPosted:)
      name:UserControllerAPIKeyChanged
      object:nil];
}

- (void)awakeFromCib
{
  // =================================================================
  // = We want the window from Cib to become our full browser window =
  // =================================================================
 
  [theWindow setFullPlatformWindow:YES];
  
  _mainView     = [theWindow contentView]
  _mainSubview  = [[CPView alloc] init]
  
  [_mainView addSubview:_mainSubview]
  
    
  // =====================
  // = Setup the toolbar =
  // =====================
  
  _toolbar = [[CPToolbar alloc] initWithIdentifier:"mainToolbar"];
  
  [_toolbar setDelegate:self];
  [_toolbar setVisible:YES];
  [theWindow setToolbar:_toolbar];
  
  // ===================================================
  // = selectedChar default value and charToolbarView  =
  // ===================================================
  
  EVSelectedCharacter = 1;
  _charImageView = [[CPImageView alloc] initWithFrame:CGRectMake(0,0,59, 59)];
  
  [self updateCharToolbarView];
  
  // =======================================================
  // = Load the login window and display it at the center  =
  // =======================================================
  
  _loginController = [[LoginController alloc] initWithWindowCibName:"LoginWindow"];
  
  [[_loginController window] center];
  [[_loginController window] setMovable:NO];
  [[_loginController window] orderFront:self];
  
}

// ============
// = Actions  =
// ============

-(@action) toolbarItemManageAccoutClicked:(id)sender
{ 
  if (_userController)
  {
    [[_userController view] setFrame:[_mainView bounds]];
    [[_userController view] setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
    
    [_mainView replaceSubview:_mainSubview with:[_userController view]];
    _mainSubview = [_userController view]
  }
  
  else
  {
    _userController = [[UserController alloc] initWithCibName:"UserView" bundle:nil];
    
    [[_userController view] setFrame:[_mainView bounds]];
    [[_userController view] setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
    
    [_mainView replaceSubview:_mainSubview with:[_userController view]];
    _mainSubview = [_userController view]
  }
}

-(@action) toolbarItemAssetsClicked:(id)sender
{
  if (_assetsController)
  {
    [[_assetsController view] setFrame:[_mainView bounds]];
    [[_assetsController view] setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
    
    [_mainView replaceSubview:_mainSubview with:[_assetsController view]];
    _mainSubview = [_assetsController view]
  }
  
  else
  {
    _assetsController = [[AssetsController alloc] initWithCibName:"AssetsView" bundle:nil];
    
    [[_assetsController view] setFrame:[_mainView bounds]];
    [[_assetsController view] setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
    
    [_mainView replaceSubview:_mainSubview with:[_assetsController view]];
    _mainSubview = [_assetsController view]
  }
}

-(@action) charChanged:(id)sender
{
  EVSelectedCharacter = [sender modelObject];
  [self updateCharToolbarView];
}

// ===================================
// = Notification Observer callbacks =
// ===================================

-(void) loginSuccessfulNotificationPosted:(id)sender
{
  //
  // Syncron apiKeys request. This triggers an APIKey update in the Backend
  //
  
  var request = [CPURLRequest requestWithURL:baseURL + eveAPIKeyURL];
  var data    = [CPURLConnection sendSynchronousRequest:request returningResponse: nil];
  
  var obj = [data JSONObject]
  [[DataSourceCache sharedCache] setApiKeys: [CPArray arrayWithObjects: obj.result]];
  
  var request = [CPURLRequest requestWithURL:baseURL + eveCharactersURL];
  _charactersConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  
  var request = [CPURLRequest requestWithURL:baseURL + eveCorporationsURL];
  _corporationsConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  
  [[_loginController window] close];
  [theWindow orderFront:self];
}

-(void) APIKeyChangedNotificationPosted:(id)sender
{
  var bundle = [CPBundle mainBundle];
  var baseURL = "http://" + [[bundle bundleURL] host] + ":" + [[bundle bundleURL] port];
  
  var request = [CPURLRequest requestWithURL:baseURL + charactersURL];
  _charactersConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

// =============================
// = CPURLConnection delegate =
// =============================

-(void) connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  var obj = CPJSObjectCreateWithJSON(data);
  
  if (connection == _charactersConnection)
  {
    var toolbarItem = nil
    
    // Find the ToolbarItem
    
    for (var i = 0; i < [_toolbar items].length; ++i)
    {
      if ([[_toolbar items][i] itemIdentifier] == CharSelectorToolbarItem)
      {
        toolbarItem = [_toolbar items][i];
      }
    }
    
    // Add all Characters to the toolbarItem View
    
    for (var i = 0; i < obj.result.length; ++i)
    {
      var menuItem = [[EVMenuItem alloc] init];
      [menuItem setTarget:self];
      [menuItem setAction:@selector(charChanged:)];
      [menuItem setTitle:obj.result[i].fields.characterName];
      [menuItem setModelObject:obj.result[i]];
        
      [[toolbarItem view] addItem: menuItem];
    }
    
    EVSelectedCharacter = [[[toolbarItem view] selectedItem] modelObject];
    [self updateCharToolbarView];
  }
  
  if (connection == _corporationsConnection)
  {
    var toolbarItem = nil
    
    // Find the ToolbarItem
    
    for (var i = 0; i < [_toolbar items].length; ++i)
    {
      if ([[_toolbar items][i] itemIdentifier] == CharSelectorToolbarItem)
      {
        toolbarItem = [_toolbar items][i];
      }
    }
  }
}

// =====================
// = Toolbar delegates =
// =====================

-(CPArray)toolbarAllowedItemIdentifiers:(CPToolbar)aToolbar
{
  return [
    CPToolbarFlexibleSpaceItemIdentifier,
    CharImagePlaceholderToolbarItem,
    CharSelectorToolbarItem,
    ManageAccountToolbarItem,
    AssetsToolbarItem
  ];
}

-(CPArray)toolbarDefaultItemIdentifiers:(CPToolbar)aToolbar
{
  return [
    CharImagePlaceholderToolbarItem,
    CharSelectorToolbarItem,
    CPToolbarFlexibleSpaceItemIdentifier,
    AssetsToolbarItem,
    ManageAccountToolbarItem,
    CPToolbarFlexibleSpaceItemIdentifier
   ];
}

-(CPToolbarItem)toolbar:(CPToolbar)aToolbar itemForItemIdentifier:(CPString)anItemIdentifier willBeInsertedIntoToolbar:(BOOL)aFlag
{
  var toolbarItem = [[CPToolbarItem alloc] initWithItemIdentifier:anItemIdentifier];

  if (anItemIdentifier == CharImagePlaceholderToolbarItem)
  {
    [toolbarItem setMinSize:CGSizeMake(59, 32)];
    [toolbarItem setMaxSize:CGSizeMake(59, 32)];
  }

  else if (anItemIdentifier == CharSelectorToolbarItem)
  {
    var selector = [[CPPopUpButton alloc] initWithFrame:CGRectMake(0,0,128, 24)];
    
    [toolbarItem setView:selector];
    [toolbarItem setLabel:"Switch Character"]
    [toolbarItem setMinSize:CGSizeMake(128, 24)];
    [toolbarItem setMaxSize:CGSizeMake(128, 24)];
  }
  
  else if (anItemIdentifier == AssetsToolbarItem)
  {
    var icon = [[CPImage alloc] initWithContentsOfFile:"./Resources/IconsToolbar/assets.png"];
    
    [toolbarItem setImage:icon];
    [toolbarItem setLabel:"Assets"];
    [toolbarItem setTarget:self];
    [toolbarItem setAction:@selector(toolbarItemAssetsClicked:)];
    [toolbarItem setMinSize:CGSizeMake(32, 32)];
    [toolbarItem setMaxSize:CGSizeMake(32, 32)];
  }
  
  else if (anItemIdentifier == ManageAccountToolbarItem)
  {
    var icon = [[CPImage alloc] initWithContentsOfFile:"./Resources/IconsToolbar/account.png"];
    
    [toolbarItem setImage:icon];
    [toolbarItem setLabel:"Account"];
    [toolbarItem setTarget:self];
    [toolbarItem setAction:@selector(toolbarItemManageAccoutClicked:)];
    [toolbarItem setMinSize:CGSizeMake(32, 32)];
    [toolbarItem setMaxSize:CGSizeMake(32, 32)];
  }
    
    return toolbarItem;
}

-(void) updateCharToolbarView
{
  [_charImageView removeFromSuperview];
  [_charImageView setImage:[[ImageCache sharedCache] getImageForObject:EVSelectedCharacter]];
  
  var toolbarView = [_toolbar _toolbarView];
  [toolbarView addSubview:_charImageView];
}

@end
