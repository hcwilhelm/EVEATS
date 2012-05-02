// 
//  AssetsController.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-04-26.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 

@import <Foundation/Foundation.j>

@import "../Utils/BackendURLS.j"
@import "../Views/EVMarketGroupOutlineView.j"

@implementation AssetsController : CPViewController
{
  @outlet CPView                  navigationView;
    @outlet CPView                navigationFilterView;
    @outlet CPSplitView           navigationSplitView;
      @outlet CPView              navigationDataView;
      @outlet CPView              navigationMetaInfoView;
        @outlet CPView            navigationMetaInfoLabelView;
    @outlet CPButtonBar           navigationButtonBar;
  @outlet CPView                  contentView;
    @outlet CPSplitView           contentSplitView;
  
  CPScrollView                    _outlineScrollView;
  EVMarketGroupOutlineView        _outlineView;
  
  CPButton                        _hideButton;
  CPImage                         _hideButtonImageDisable;
  CPImage                         _hideButtonImageEnable;
  BOOL                            _metaInfoViewVisible;
  
  CPDictionary                    _treeData;
}

-(void)awakeFromCib
{
  console.log("AssetsController awakeformCIB");
  
  // =================
  // = splitViewMain =
  // =================

  [[self view] setIsPaneSplitter:NO];
  [[self view] setPosition:250 ofDividerAtIndex:0];
  
  [navigationView setAutoresizingMask:CPViewNotSizable];
  [contentView setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
  
  // ==============
  // = filterView =
  // ==============
  
  [navigationFilterView setBackgroundColor:[CPColor colorWithPatternImage:[[CPImage alloc] initWithContentsOfFile:"./Resources/Backgrounds/background-filter.png"]]];
  
  // =======================
  // = navigationSplitView =
  // =======================
  
  [navigationSplitView setIsPaneSplitter:NO];
  
  [navigationDataView setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
  [navigationMetaInfoView setAutoresizingMask:CPViewNotSizable];
  
  // =====================
  // = metaInfoLabelView =
  // =====================
  
  [navigationMetaInfoLabelView setBackgroundColor:[CPColor colorWithPatternImage:[[CPImage alloc] initWithContentsOfFile:"./Resources/Backgrounds/background-filter.png"]]];
  
  // ===========================
  // = navigationAreaButtonBar =
  // ===========================
  
  var bezelColor              = [CPColor colorWithPatternImage:[[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarBackground.png"]];
  
  var leftBezel               = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarLeftBezel.png"];
  var centerBezel             = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarCenterBezel.png"];
  var rightBezel              = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarRightBezel.png"];
  var buttonBezel             = [CPColor colorWithPatternImage:[[CPThreePartImage alloc] initWithImageSlices:[leftBezel, centerBezel, rightBezel] isVertical:NO]];
  
  var leftBezelHighlighted    = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarLeftBezelHighlighted.png"];
  var centerBezelHighlighted  = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarCenterBezelHighlighted.png"];
  var rightBezelHighlighted   = [[CPImage alloc] initWithContentsOfFile:"./Resources/TNButtonBar/buttonBarRightBezelHighlighted.png"];
  var buttonBezelHighlighted  = [CPColor colorWithPatternImage:[[CPThreePartImage alloc] initWithImageSlices:[leftBezelHighlighted, centerBezelHighlighted, rightBezelHighlighted] isVertical:NO]];
  
  [navigationButtonBar setValue:bezelColor forThemeAttribute:"bezel-color"];
  [navigationButtonBar setValue:buttonBezel forThemeAttribute:"button-bezel-color"];
  [navigationButtonBar setValue:buttonBezelHighlighted forThemeAttribute:"button-bezel-color" inState:CPThemeStateHighlighted];
  
  _hideButtonImageEnable  = [[CPImage alloc] initWithContentsOfFile:"./Resources/IconsButtonBar/show.png"];
  _hideButtonImageDisable = [[CPImage alloc] initWithContentsOfFile:"./Resources/IconsButtonBar/hide.png"];
  
  _hideButton = [CPButtonBar minusButton];
  [_hideButton setImage:_hideButtonImageDisable];
  [_hideButton setToolTip:"Display or hide the info view"];
  [_hideButton setTarget:self];
  [_hideButton setAction:@selector(toggleMetaInfoView:)];
  
  _metaInfoViewVisible = YES;
  
  var buttons = [CPArray array];
  [buttons addObject:_hideButton];
  
  [navigationButtonBar setButtons:buttons];
  
  // ================
  // = OutlineView  =
  // ================
  
  _outlineScrollView = [[CPScrollView alloc] initWithFrame:[navigationDataView bounds]];
  [_outlineScrollView setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
  [_outlineScrollView setAutohidesScrollers:YES];
  
  _outlineView = [[EVMarketGroupOutlineView alloc] initWithFrame:[navigationDataView bounds]];
  [_outlineView setDelegate:self];
  [_outlineView setEnabled:NO];
  
  
  [_outlineScrollView setDocumentView:_outlineView];
  [navigationDataView addSubview:_outlineScrollView];
  
  [self loadTreeData]
}

-(void) loadTreeData
{
  var request     = [CPURLRequest requestWithURL:baseURL + eveMarketGroupTreeURL];
  var connection  = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(@action) toggleMetaInfoView:(id)sender
{
  if (_metaInfoViewVisible)
  {
    [navigationMetaInfoView removeFromSuperview];
    [_hideButton setImage:_hideButtonImageEnable];
    _metaInfoViewVisible = NO;
  }
  
  else 
  {
    [navigationSplitView addSubview:navigationMetaInfoView];
    [navigationSplitView setPosition:[navigationMetaInfoView frame].origin.y ofDividerAtIndex:0];
    [_hideButton setImage:_hideButtonImageDisable];
    _metaInfoViewVisible = YES;
  }
}

// =============================
// = CPURLConnection Delegates =
// =============================

-(void) connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  _treeData = [CPDictionary dictionaryWithJSObject: CPJSObjectCreateWithJSON(data) recursively:YES]

  [_outlineView setDataSource:self];
  [_outlineView setEnabled:YES];
}

// ====================================
// = OutlineView DataSource delegates =
// ====================================

-(id) outlineView:(CPOutlineView)outlineView child:(CPInteger)index ofItem:(id)item
{
  if (item)
  {
    return [[item objectForKey:@"childs"] objectAtIndex:index];
  }
  
  else
  {
    return [_treeData objectForKey:index];
  }
} 

-(BOOL) outlineView:(CPOutlineView)outlineView isItemExpandable:(id)item
{
  if ([[item objectForKey:@"childs"] count] > 0)
  {
    return YES;
  }
  
  else
  {
    return NO;
  }
} 

-(int) outlineView:(CPOutlineView)outlineView numberOfChildrenOfItem:(id)item
{
  if (item)
  {
    return [[item objectForKey:@"childs"] count];
  }
  
  else
  {
    return [_treeData count];
  }
} 

-(id) outlineView:(CPOutlineView)outlineView objectValueForTableColumn:(CPTableColumn)tableColumn byItem:(id)item
{
  return item;
}

// =========================
// = OutlineView delegates =
// =========================

-(void) outlineViewSelectionDidChange:(CPNotification)notification
{
  console.log(notification);
}


@end