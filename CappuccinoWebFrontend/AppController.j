/*
 * AppController.j
 * EveAssets
 *
 * Created by You on April 10, 2011.
 * Copyright 2011, Your Company All rights reserved.
 */

@import <Foundation/CPObject.j>
@import "EAMarketGroupView.j"

/* ================================ */
/* = CPToolBar identifier strings = */
/* ================================ */

var searchFieldToolbarItemIdentifier = "searchFieldToolbarItemIdentifier";


/* ================ */
/* = AppContorler = */
/* ================ */

@implementation AppController : CPObject
{
	CPWindow 			theWindow;
	CPToolbar 			toolbar;
	CPSearchField		searchField;
	
	EAMarketGroupView 	marketGroupView;
}

- (void)applicationDidFinishLaunching:(CPNotification)aNotification
{
    theWindow	= [[CPWindow alloc] initWithContentRect:CGRectMakeZero() styleMask:CPBorderlessBridgeWindowMask],
    contentView = [theWindow contentView];

	[self createToolbar];

	marketGroupView = [[EAMarketGroupView alloc] initWithFrame:[contentView bounds]];
	[contentView addSubview:marketGroupView];

    [theWindow orderFront:self];

    // Uncomment the following line to turn on the standard menu bar.
    //[CPMenu setMenuBarVisible:YES];
}

-(void)createToolbar
{
	toolbar = [[CPToolbar alloc] initWithIdentifier:"Main Tools"];
	[toolbar setDelegate:self];
	[toolbar setVisible:YES];

	[theWindow setToolbar: toolbar];
}

/* ======================= */
/* = CPToolbar Delegates = */
/* ======================= */

-(CPArray) toolbarAllowedItemIdentifiers:(CPToolbar)aToolbar
{
	return [searchFieldToolbarItemIdentifier, CPToolbarFlexibleSpaceItemIdentifier]
}

-(CPArray) toolbarDefaultItemIdentifiers:(CPToolbar)aToolbar
{
	return [CPToolbarFlexibleSpaceItemIdentifier, searchFieldToolbarItemIdentifier]
}

-(CPToolbarItem) toolbar:(CPToolbar)aToolbar itemForItemIdentifier:(CPString)anItemIdentifier willBeInsertedIntoToolbar:(BOOL)aFlag
{
	var toolbarItem = [[CPToolbarItem alloc] initWithItemIdentifier:anItemIdentifier];
	
	if (anItemIdentifier == searchFieldToolbarItemIdentifier)
	{
		var searchField = [[CPSearchField alloc] initWithFrame:CGRectMake(0, 10, 200, 30)];
		[searchField setTarget:self];
		[searchField setAction:@selector(getItemTypes:)];
		[toolbarItem setView:searchField];

		[toolbarItem setMinSize:CGSizeMake(200, 30)];
		[toolbarItem setMaxSize:CGSizeMake(200, 30)];
	}
	
	return toolbarItem;
}

/* ====================== */
/* = SearchField action = */
/* ====================== */

-(void) getItemTypes:(id)sender
{	
	var request			= [CPURLRequest requestWithURL:@"http://46.4.97.35:8000/assets/listCorpAssetsByName/" + "?name=" + [sender objectValue]];
	var connection		= [CPURLConnection connectionWithRequest:request delegate:self];
	
	console.log([sender objectValue]);
}

-(void) connection:(CPURLConnection)aConnection didReceiveData:(CPString)data
{
	var _data = [CPData dataWithJSONObject:JSON.parse(data)];
	
	[[[marketGroupView detailTableView] dataSource] setData: _data];
	
}

-(void) connection:(CPURLConnection)connection didFailWithError:(id)error
{
	[connection cancel];
}
@end
