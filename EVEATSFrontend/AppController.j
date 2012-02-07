/*
 * AppController.j
 * testApp
 *
 * Created by You on February 1, 2012.
 * Copyright 2012, Your Company All rights reserved.
 */

@import <Foundation/CPObject.j>

@import "LoginController.j"
@import "UserController.j"
@import "ImageCache.j"

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
    @outlet CPSplitView   verticalSplitView;
    @outlet CPView        filterView;
    @outlet CPView        infoLabelView;
    @outlet CPButtonBar   leftButtonBar;
    
    CPToolbar             _toolbar;
    CPWindowController    _loginController;
    CPViewController      _userController;
    
    CPButton              _hideButton;
    CPImage               _hideButtonImageDisable;
    CPImage               _hideButtonImageEnable;
}

- (void)applicationDidFinishLaunching:(CPNotification)aNotification
{
    // This is called when the application is done loading.
    
    [[CPNotificationCenter defaultCenter] 
      addObserver:self
      selector:@selector(loginSuccessfulNotificationPosted:)
      name:LoginControllerLoginSuccessful
      object:nil];
      
    userController = [[UserController alloc] initWithCibName:"UserView" bundle:nil];
    [[userController view] setFrame:[[theWindow contentView] frame]];
    
    console.log(theWindow);
    console.log([userController view]);
    //[theWindow setContentView:[userController view]];
    
    
}

- (void)awakeFromCib
{
  // =================================================================
  // = We want the window from Cib to become our full browser window =
  // =================================================================
 
  [theWindow setFullPlatformWindow:YES];
    
  // =====================
  // = Setup the toolbar =
  // =====================
  
  _toolbar = [[CPToolbar alloc] initWithIdentifier:"mainToolbar"];
  
  [_toolbar setDelegate:self];
  [_toolbar setVisible:YES];
  [theWindow setToolbar:_toolbar];
  
  [self createCharToolbarView];
  
  // =======================================================
  // = Load the login window and display it at the center  =
  // =======================================================
  
  _loginController = [[LoginController alloc] initWithWindowCibName:"LoginWindow"];
  
  [[_loginController window] center];
  [[_loginController window] setMovable:NO];
  [[_loginController window] orderFront:self];
  
  
  // =====================
  // = verticalSplitView =
  // =====================

  [verticalSplitView setIsPaneSplitter:NO];
  
  // ===============
  // = Filter View =
  // ===============
  
  [filterView setBackgroundColor:[CPColor colorWithPatternImage:[[CPImage alloc] initWithContentsOfFile:"./Resources/Backgrounds/background-filter.png"]]];
  
  // =================
  // = infoLabelView =
  // =================
  
  [infoLabelView setBackgroundColor:[CPColor colorWithPatternImage:[[CPImage alloc] initWithContentsOfFile:"./Resources/Backgrounds/background-filter.png"]]];
  
  // =================
  // = leftButtonBar =
  // =================
  
  var bezelColor              = [CPColor colorWithPatternImage:[[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarBackground.png"]];
  
  var leftBezel               = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarLeftBezel.png"];
  var centerBezel             = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarCenterBezel.png"];
  var rightBezel              = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarRightBezel.png"];
  var buttonBezel             = [CPColor colorWithPatternImage:[[CPThreePartImage alloc] initWithImageSlices:[leftBezel, centerBezel, rightBezel] isVertical:NO]];
  
  var leftBezelHighlighted    = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarLeftBezelHighlighted.png"];
  var centerBezelHighlighted  = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarCenterBezelHighlighted.png"];
  var rightBezelHighlighted   = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarRightBezelHighlighted.png"];
  var buttonBezelHighlighted  = [CPColor colorWithPatternImage:[[CPThreePartImage alloc] initWithImageSlices:[leftBezelHighlighted, centerBezelHighlighted, rightBezelHighlighted] isVertical:NO]];
  
  [leftButtonBar setValue:bezelColor forThemeAttribute:"bezel-color"];
  [leftButtonBar setValue:buttonBezel forThemeAttribute:"button-bezel-color"];
  [leftButtonBar setValue:buttonBezelHighlighted forThemeAttribute:"button-bezel-color" inState:CPThemeStateHighlighted];
  
  _hideButtonImageEnable  = [[CPImage alloc] initWithContentsOfFile:"./Resources/IconsButtonBar/show.png"];
  _hideButtonImageDisable = [[CPImage alloc] initWithContentsOfFile:"./Resources/IconsButtonBar/hide.png"];
  
  _hideButton             = [CPButtonBar minusButton];
  [_hideButton setImage:_hideButtonImageEnable];
  
  var buttons = [CPArray array];
  [buttons addObject:_hideButton];
  
  [leftButtonBar setButtons:buttons];
  
}

// ===================================
// = Notification Observer callbacks =
// ===================================

-(void) loginSuccessfulNotificationPosted:(id)sender
{
  [[_loginController window] close];
  [theWindow orderFront:self];
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
    ManageAccountToolbarItem,
    AssetsToolbarItem
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
    
    return toolbarItem;
}

-(void) createCharToolbarView
{
  var charImageView = [[CPImageView alloc] initWithFrame:CGRectMake(0,0,59, 59)];
  [charImageView setImage:[[ImageCache sharedCache] getCharImageForID:"1"]];
  
  var toolbarView = [_toolbar _toolbarView];
  [toolbarView addSubview:charImageView];
}

@end
