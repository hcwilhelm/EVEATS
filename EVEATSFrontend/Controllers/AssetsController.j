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


// =================
// = Notifications =
// =================

AppControllerCharChanged = @"AppControllerCharChanged";


@implementation AssetsController : CPViewController
{
  @outlet CPView                  navigationView;
    @outlet CPView                navigationFilterView;
      @outlet CPSearchField       searchField;
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
  
  CPProgressIndicator             _progressIndicator;
  
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
  
  // ===============
  // = SearchField =
  // ===============
  
  [searchField setTarget:self];
  [searchField setAction:@selector(getAssetsByName:)];
  
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
  [_assetTableView setColumnAutoresizingStyle:CPTableViewLastColumnOnlyAutoresizingStyle];
  [_assetTableView setRowHeight: 32];
  [_assetTableView setDataSource:self];
  [_assetTableView setDelegate:self];

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
  
  var quantityColumn = [[CPTableColumn alloc] initWithIdentifier:@"quantityColumn"];
  [[quantityColumn headerView] setStringValue:@"Quantity"];
  
  [_assetTableView addTableColumn:iconColumn];
  [_assetTableView addTableColumn:typeNameColumn];
  [_assetTableView addTableColumn:locationNameColumn];
  [_assetTableView addTableColumn:quantityColumn];
  
  [_assetScrollView setDocumentView:_assetTableView];
  [assetView addSubview: _assetScrollView]
  
  // =====================
  // = Asset Detail View =
  // =====================
  
  _assetDetailScrollView = [[CPScrollView alloc] initWithFrame:[asserDetailView bounds]];
  [_assetDetailScrollView setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
  [_assetDetailScrollView setAutohidesScrollers:YES];
  
  _assetDetailOutlineView = [[CPOutlineView alloc] initWithFrame:[navigationDataView bounds]];

  var iconColumn = [[CPTableColumn alloc] initWithIdentifier:@"iconColumn"];
  [[iconColumn headerView] setStringValue:@"Icon"];
  
  var iconView = [[EVTableColumnIconView alloc] initWithFrame:CPRectMake(0,0,32, 32)];
  [iconColumn setDataView:iconView];
  [iconColumn setWidth: 100]
  
  var typeNameColumn = [[CPTableColumn alloc] initWithIdentifier:@"typeNameColumn"];
  [[typeNameColumn headerView] setStringValue:@"TypeName"];
  [typeNameColumn setWidth: 300]
  
  var flagColumn = [[CPTableColumn alloc] initWithIdentifier:@"flagColumn"];
  [[flagColumn headerView] setStringValue:@"Flag"];
  
  var quantityColumn = [[CPTableColumn alloc] initWithIdentifier:@"quantityColumn"];
  [[quantityColumn headerView] setStringValue:@"Quantity"];
  
  [_assetDetailOutlineView setAutoresizingMask:CPViewHeightSizable | CPViewWidthSizable];
  [_assetDetailOutlineView setRowHeight:32];
  [_assetDetailOutlineView setColumnAutoresizingStyle:CPTableViewLastColumnOnlyAutoresizingStyle];
  [_assetDetailOutlineView addTableColumn:iconColumn];
  [_assetDetailOutlineView addTableColumn:typeNameColumn];
  [_assetDetailOutlineView addTableColumn:flagColumn];
  [_assetDetailOutlineView addTableColumn:quantityColumn];
  [_assetDetailOutlineView setOutlineTableColumn:iconColumn];
  [_assetDetailOutlineView setDataSource:self];
  
  [_assetDetailScrollView setDocumentView:_assetDetailOutlineView];
  [asserDetailView addSubview:_assetDetailScrollView];
  
  // ========================
  // = Import Progress View =
  // ========================

  _progressIndicator = [[CPProgressIndicator alloc] initWithFrame:CGRectMake(0,0,256,16)];
  [_progressIndicator setStyle:CPProgressIndicatorBarStyle];
  
  //var progress = [[CPProgressIndicator alloc] initWithFrame:CGRectMakeZero()];
  //[progress setStyle:CPProgressIndicatorSpinningStyle];
  //[progress sizeToFit];
  
  //[progressIndicator addSubview: progress];
  
  //var p = [[CPProgressIndicator alloc] initWithFrame:CGRectMake(100,100,256,16)];
  //[p setStyle:CPProgressIndicatorBarStyle];
  //[p setMaxValue: 1000.0];
  //[p setMinValue: 0.0];
  //[p setDoubleValue: 344.0];
  //[p setIndeterminate:YES];
  //[p startAnimation:self];
  
  //[p sizeToFit];
  
  //[asserDetailView addSubview: p];
  
  // =============================
  // = Load the MarketGroup Tree =
  // =============================
  
  [self loadTreeData]
  
  // ========================
  // = Register as Observer =
  // ========================
  
  [[CPNotificationCenter defaultCenter] 
    addObserver:self
    selector:@selector(appControllerCharChanged:)
    name:AppControllerCharChanged
    object:nil];
}

-(void) loadTreeData
{
  var request         = [CPURLRequest requestWithURL:baseURL + eveMarketGroupTreeURL];
  _treeDataConnection = [CPURLConnection connectionWithRequest:request delegate:self];
}

-(void) appControllerCharChanged:(id)sender
{
  _assetData        = [[CPDictionary alloc] init];
  _assetDetailData  = [[CPDictionary alloc] init];
  
  [_assetTableView reloadData];
  [_assetDetailOutlineView reloadData];
  [searchField setStringValue:@""];
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
        var containerSize = [assetView frame].size;
        var elementSize   = [_progressIndicator frame].size;
        
        [_progressIndicator setFrame: CGRectMake(containerSize.width/2.0 - elementSize.width/2.0, containerSize.height/2.0 - elementSize.height/2.0, 256, 16)];
        [_progressIndicator setAutoresizingMask:  CPViewMinXMargin | CPViewMaxXMargin | CPViewMinYMargin | CPViewMaxYMargin];
                                    
        [assetView replaceSubview:_assetScrollView with:_progressIndicator];
        
        var request             = [CPURLRequest requestWithURL:baseURL + "/tasks/" + json.taskID + "/status"];
        _taskProgressConnection = [CPURLConnection connectionWithRequest:request delegate:self];
      }
    }
  }
  
  if (connection == _taskProgressConnection)
  {
    json = CPJSObjectCreateWithJSON(data);
    
    if (json.task.status == "PENDING")
    {
      var request = [CPURLRequest requestWithURL:baseURL + "/tasks/" + json.task.id + "/status"];
      
      window.setTimeout(function() { 
          _taskProgressConnection = [CPURLConnection connectionWithRequest:request delegate:self];
        }, 500);
    }
    
    if (json.task.status == "PROGRESS")
    {
      var request = [CPURLRequest requestWithURL:baseURL + "/tasks/" + json.task.id + "/status"];
      
      [_progressIndicator setMinValue: 0.0];
      [_progressIndicator setMaxValue: json.task.result.total];
      [_progressIndicator setDoubleValue: json.task.result.current];
      
      window.setTimeout(function() { 
          _taskProgressConnection = [CPURLConnection connectionWithRequest:request delegate:self];
        }, 500);
    }
    
    if (json.task.status == "SUCCESS")
    {
      [_assetScrollView setFrame: [assetView bounds]];
      [assetView replaceSubview:_progressIndicator with:_assetScrollView];
    }
    
  }
  
  if (connection == _assetDetailDataConnection)
  {
    json = CPJSObjectCreateWithJSON(data);
    
    if (json.success)
    {
      _assetDetailData = [CPDictionary dictionaryWithJSObject: json.result recursively:YES];
      [_assetDetailOutlineView reloadData];
    }
  }
}

-(void) connection:(CPURLConnection)connection didFailWithError:(id)error
{
  console.log("Connection error");
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
  
  if ([aColumn identifier] == @"quantityColumn")
  {
    return [[_assetData objectForKey:aRowIndex] objectForKey:@"quantity"];
  }
}

// ====================================
// = OutlineView DataSource delegates =
// ====================================

-(id) outlineView:(CPOutlineView)outlineView child:(CPInteger)index ofItem:(id)item
{
  if (outlineView == _outlineView)
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
  
  if (outlineView == _assetDetailOutlineView)
  {
    if (item)
    {
      return [[item objectForKey:@"childs"] objectAtIndex:index];
    }
    
    else
    {
      return [_assetDetailData objectForKey:index];
    }
  }
  
} 

-(BOOL) outlineView:(CPOutlineView)outlineView isItemExpandable:(id)item
{
  if (outlineView == _outlineView)
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
  
  if (outlineView == _assetDetailOutlineView)
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
  
}

-(int) outlineView:(CPOutlineView)outlineView numberOfChildrenOfItem:(id)item
{
  if (outlineView == _outlineView)
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
  
  if (outlineView == _assetDetailOutlineView)
  {
    if (item)
    {
      return [[item objectForKey:@"childs"] count];
    }

    else
    {
      return [_assetDetailData count];
    }
  }
  
} 

-(id) outlineView:(CPOutlineView)outlineView objectValueForTableColumn:(CPTableColumn)tableColumn byItem:(id)item
{
  if (outlineView == _outlineView)
  {
    return item;
  }
  
  if (outlineView == _assetDetailOutlineView)
  {
    if ([tableColumn identifier] == @"iconColumn")
    {
      return [item objectForKey:@"typeID"];
    }
    
    if ([tableColumn identifier] == @"typeNameColumn")
    {
      return [item objectForKey:@"typeName"];
    }
    
    if ([tableColumn identifier] == @"flagColumn")
    {
      return [item objectForKey:@"flag"];
    }
    
    if ([tableColumn identifier] == @"quantityColumn")
    {
      return [item objectForKey:@"quantity"];
    }
  }
 
}

// =========================
// = OutlineView delegates =
// =========================

-(void) outlineViewSelectionDidChange:(CPNotification)notification
{
  if ([notification object] == _outlineView)
  {
    var item = [[notification object] itemAtRow:[[notification object] selectedRow]];
    
    var request = nil;
    
    if (EVSelectedCharacter.model == @"eve.character")
    {
      request = [CPURLRequest requestWithURL:baseURL + eveCharacterAssetsByGroup + EVSelectedCharacter.pk + "/" + [item objectForKey:@"marketGroupID"]];
    }

    if (EVSelectedCharacter.model == @"eve.corporation")
    {
      request = [CPURLRequest requestWithURL:baseURL + eveCorporationAssetsByGroup + EVSelectedCharacter.pk + "/" + [item objectForKey:@"marketGroupID"]];
    }
    
    _assetDataConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  }

}

// =======================
// = TableView delegates =
// =======================

-(void) tableViewSelectionDidChange:(CPNotification)notification
{
  
  if ([notification object] == _assetTableView)
  {
    var item = [_assetData objectForKey:[[notification object] selectedRow]];
    
    if ([item objectForKey:@"typeID"])
    {
      var request = nil; //[CPURLRequest requestWithURL:baseURL + eveCharacterAssetsDetailTree + EVSelectedCharacter.pk + "/" + [item objectForKey:@"typeID"] + "/" + [item objectForKey:@"locationID"]];
      
      if (EVSelectedCharacter.model == @"eve.character")
      {
        request = [CPURLRequest requestWithURL:baseURL + eveCharacterAssetsDetailTree + EVSelectedCharacter.pk + "/" + [item objectForKey:@"typeID"] + "/" + [item objectForKey:@"locationID"]];
      }

      if (EVSelectedCharacter.model == @"eve.corporation")
      {
        request = [CPURLRequest requestWithURL:baseURL + eveCorporationAssetsDetailTree + EVSelectedCharacter.pk + "/" + [item objectForKey:@"typeID"] + "/" + [item objectForKey:@"locationID"]];
      }
      
      _assetDetailDataConnection = [CPURLConnection connectionWithRequest:request delegate:self];
    }
  }
    
}

// ======================
// = SearchField Action =
// ======================

-(void) getAssetsByName:(id)sender
{
  if ([sender stringValue].match(/\w\s*/) )
  {
    var request = nil; //[CPURLRequest requestWithURL:baseURL + eveCharacterAssetsByName + EVSelectedCharacter.pk + "/" + [sender stringValue]];
    
    if (EVSelectedCharacter.model == @"eve.character")
    {
      request = [CPURLRequest requestWithURL:baseURL + eveCharacterAssetsByName + EVSelectedCharacter.pk + "/" + [sender stringValue]];
    }

    if (EVSelectedCharacter.model == @"eve.corporation")
    {
      request = [CPURLRequest requestWithURL:baseURL + eveCorporationAssetsByName + EVSelectedCharacter.pk + "/" + [sender stringValue]];
    }
    
    _assetDataConnection = [CPURLConnection connectionWithRequest:request delegate:self];
  }
  
  else
  {
    return;
  }
  
}

@end