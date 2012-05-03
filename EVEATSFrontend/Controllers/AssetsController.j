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
@import "../Views/EVTableColumnIconView.j"

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
      @outlet CPView              assetView;
      @outlet CPView              asserDetailView;
  
  CPScrollView                    _outlineScrollView;
  EVMarketGroupOutlineView        _outlineView;
  
  CPScrollView                    _assetScrollView;
  CPTableView                     _assetTableView;
  
  CPScrollView                    _assetDetailScrollView;
  CPOutlineView                   _assetDetailOutlineView;
  
  CPProgressIndicator             _assetProgressIndicator;
  
  CPButton                        _hideButton;
  CPImage                         _hideButtonImageDisable;
  CPImage                         _hideButtonImageEnable;
  BOOL                            _metaInfoViewVisible;
  
  CPDictionary                    _treeData;
  CPDictionary                    _assetData;
  CPDictionary                    _assetDetailData;
  
  CPURLConnection                 _treeDataConnection;
  CPURLConnection                 _assetDataConnection;
  CPURLConnection                 _assetDetailDataConnection;
  CPURLConnection                 _taskProgressConnection;
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
  
  // ============================
  // = MarketGroup OutlineView  =
  // ============================
  
  _outlineScrollView = [[CPScrollView alloc] initWithFrame:[navigationDataView bounds]];
  [_outlineScrollView setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
  [_outlineScrollView setAutohidesScrollers:YES];
  
  _outlineView = [[EVMarketGroupOutlineView alloc] initWithFrame:[navigationDataView bounds]];
  [_outlineView setDelegate:self];
  [_outlineView setEnabled:NO];
  
  
  [_outlineScrollView setDocumentView:_outlineView];
  [navigationDataView addSubview:_outlineScrollView];
  
  // ===================
  // = Asset TableView =
  // ===================
  
  _assetScrollView = [[CPScrollView alloc] initWithFrame:[assetView bounds]];
  [_assetScrollView setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
  [_assetScrollView setAutohidesScrollers:YES];
  
  _assetTableView = [[CPTableView alloc] initWithFrame:[assetView bounds]];
  [_assetTableView setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
  [_assetTableView setUsesAlternatingRowBackgroundColors:YES]
  [_assetTableView setCornerView:nil];
  [_assetTableView setRowHeight: 32];
  [_assetTableView setDataSource:self];

  var iconColumn = [[CPTableColumn alloc] initWithIdentifier:@"iconColumn"];
  [[iconColumn headerView] setStringValue:@"Icon"];
  
  var iconView = [[EVTableColumnIconView alloc] initWithFrame:CPRectMake(0,0,32, 32)];
  [iconColumn setDataView:iconView];
  [iconColumn setWidth: 40];
  
  var typeNameColumn = [[CPTableColumn alloc] initWithIdentifier:@"typeNameColumn"];
  [[typeNameColumn headerView] setStringValue:@"Name"];
  [typeNameColumn setWidth: 300];
  
  var locationNameColumn = [[CPTableColumn alloc] initWithIdentifier:@"locationNameColumn"];
  [[locationNameColumn headerView] setStringValue:@"Location"];
  [locationNameColumn setWidth: 400];
  
  var flagColumn = [[CPTableColumn alloc] initWithIdentifier:@"flagColumn"];
  [[flagColumn headerView] setStringValue:@"Flag"];
  
  var quantityColumn = [[CPTableColumn alloc] initWithIdentifier:@"quantityColumn"];
  [[quantityColumn headerView] setStringValue:@"Quantity"];
  
  var singletonColumn = [[CPTableColumn alloc] initWithIdentifier:@"singletonColumn"];
  [[singletonColumn headerView] setStringValue:@"Singleton"];
  
  [_assetTableView addTableColumn:iconColumn];
  [_assetTableView addTableColumn:typeNameColumn];
  [_assetTableView addTableColumn:locationNameColumn];
  [_assetTableView addTableColumn:flagColumn];
  [_assetTableView addTableColumn:quantityColumn];
  [_assetTableView addTableColumn:singletonColumn];
  
  [_assetScrollView setDocumentView:_assetTableView];
  [assetView addSubview:_assetScrollView];
  
  // ========================
  // = Import Progress View =
  // ========================

  _assetProgressIndicator = [[CPProgressIndicator alloc] initWithFrame:CGRectMakeZero()];
  [_assetProgressIndicator setStyle:CPProgressIndicatorSpinningStyle];
  [_assetProgressIndicator sizeToFit];
  [_assetProgressIndicator setAutoresizingMask:CPViewMinXMargin | CPViewMaxXMargin | CPViewMinYMargin | CPViewMaxYMargin];
  [_assetProgressIndicator setFrameOrigin:CGPointMake((CGRectGetWidth([assetView bounds]) - [_assetProgressIndicator frame].size.width) / 2.0, (CGRectGetHeight([assetView bounds]) - [_assetProgressIndicator frame].size.height) / 2.0)];
  
  
  // =============================
  // = Load the MarketGroup Tree =
  // =============================
  
  [self loadTreeData]
}

-(void) loadTreeData
{
  var request         = [CPURLRequest requestWithURL:baseURL + eveMarketGroupTreeURL];
  _treeDataConnection = [CPURLConnection connectionWithRequest:request delegate:self];
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
  if (connection == _treeDataConnection)
  {
    _treeData = [CPDictionary dictionaryWithJSObject: CPJSObjectCreateWithJSON(data) recursively:YES];

    [_outlineView setDataSource:self];
    [_outlineView setEnabled:YES];
  }
  
  if (connection == _assetDataConnection)
  {
    json = CPJSObjectCreateWithJSON(data);
    
    if (json.success)
    {
      if (json.taskID == null)
      {
        _assetData = [CPDictionary dictionaryWithJSObject: json.result recursively:YES];
        [_assetTableView reloadData];
      }
      
      else
      {
        var request             = [CPURLRequest requestWithURL:baseURL + "/tasks/" + json.taskID + "/status"];
        _taskProgressConnection = [CPURLConnection connectionWithRequest:request delegate:self];
        
        [_assetProgressIndicator setFrameOrigin:CGPointMake((CGRectGetWidth([assetView bounds]) - [_assetProgressIndicator frame].size.width) / 2.0, (CGRectGetHeight([assetView bounds]) - [_assetProgressIndicator frame].size.height) / 2.0)];
        [assetView replaceSubview:_assetScrollView with:_assetProgressIndicator];
      }
    }
  }
  
  if (connection == _taskProgressConnection)
  {
    json = CPJSObjectCreateWithJSON(data);
    
    if (json.task.status == "PENDING")
    {
      var request             = [CPURLRequest requestWithURL:baseURL + "/tasks/" + json.task.id + "/status"];
      
      window.setTimeout(function() { 
          _taskProgressConnection = [CPURLConnection connectionWithRequest:request delegate:self];
        }, 500);
    }
    
    else 
    {
      [assetView replaceSubview:_assetProgressIndicator with:_assetScrollView];
    }
    
  }
}

// ==================================
// = TableView DataSource delegates =
// ==================================

-(int) numberOfRowsInTableView:(CPTableView)aTableView
{
  return [_assetData count];
}

-(id) tableView:(CPTableView)aTableView objectValueForTableColumn:(CPTableColumn)aColumn row:(int)aRowIndex
{
  if ([aColumn identifier] == @"iconColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"typeID"];
  }
  
  if ([aColumn identifier] == @"typeNameColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"typeName"];
  }
  
  if ([aColumn identifier] == @"locationNameColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"locationName"];
  }
  
  if ([aColumn identifier] == @"flagColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"flag"];
  }
  
  if ([aColumn identifier] == @"quantityColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"quantity"];
  }
  
  if ([aColumn identifier] == @"singletonColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"singleton"];
  }
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
  var item = [[notification object] itemAtRow:[[notification object] selectedRow]];
  var request = [CPURLRequest requestWithURL:baseURL + eveCharacterAssets + EVSelectedCharacter.pk + "/" + [item objectForKey:@"marketGroupID"]];
  
  _assetDataConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}


@end