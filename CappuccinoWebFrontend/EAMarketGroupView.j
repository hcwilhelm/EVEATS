/*
   EAMarketGroupView.j
   EVEAssets
   
   Created by Hans Christian Wilhelm on 2011-05-03.
   Copyright 2011 Scienceondope.org All rights reserved.
*/

@import <Foundation/CPObject.j>
@import <AppKit/CPView.j>

/* ============================= */
/* = File Scope shared objects = */
/* ============================= */

/* ===================== */
/* = Cache Dictionarys = */
/* ===================== */
var _marketGroupsDictionary		= [[CPDictionary alloc] init];
var _eveTypeDictionary			= [[CPDictionary alloc] init];
var _eveSmallIconsDictionary	= [[CPDictionary alloc] init];
var _eveTypeIconsDictionary		= [[CPDictionary alloc] init];

/* ================= */
/* = DB Query URLS = */
/* ================= */
var _marketGroupsURL 			= @"http://scienceondope.org/EVEATS_BACKEND/assets/marketGroups/"
var _eveIconListURL				= @"http://scienceondope.org/EVEATS_BACKEND/assets/listEveIcons/"
var _listCorpAssetsURL			= @"http://scienceondope.org/EVEATS_BACKEND/assets/listCorpAssets/"
var _getTreeForTypeIDURL		= @"http://scienceondope.org/EVEATS_BACKEND/assets/getTreeForTypeID/"

/* ========================= */
/* = Eve static image dump = */
/* ========================= */
var _eveSmallIconsURL			= @"http://scienceondope.org:81/EveAssets/Resources/ccp_image_dump/icons/16_16/icon"
var _eveDefaultIconURL			= @"http://scienceondope.org:81/EveAssets/Resources/list_view_16x16.png"
var _eveTypesIconsURL			= @"http://scienceondope.org:81/EveAssets/Resources/ccp_image_dump/types"


@implementation EAMarketGroupView : CPView
{
	/* ======================================== */
	/* = Indentation to reflect the hirarchie = */
	/* ======================================== */
	CPSplitView 				_splitVertical			@accessors(property=splitVertical);
		CPScrollView			_navigationArea			@accessors(property=navigationArea);
			CPOutlineView		_outlineView			@accessors(property=outlineView);
		CPSplitView 			_contentView			@accessors(property=contentView);
			CPScrollView		_detailArea				@accessors(property=detailArea);
				CPTableView		_detailTableView		@accessors(property=detailTableView);
			CPScrollView		_detailView				@accessors(property=detailView);
				CPOutlineView	_detailOutlineView		@accessors(property=detailOutlineView);
}

-(id) initWithFrame:(CGRect)aFrame
{
	self = [super initWithFrame:aFrame];
	
	if(self)
	{
		[self setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
		
		_splitVertical = [[CPSplitView alloc] initWithFrame:[super bounds]];
		[_splitVertical setVertical:YES];
		[_splitVertical setIsPaneSplitter:YES];
		[_splitVertical setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
		
		_navigationArea = [[CPScrollView alloc] initWithFrame:CGRectMake(0, 0, 300, CGRectGetHeight([_splitVertical bounds]))];
		//[_navigationArea setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
		[_navigationArea setAutohidesScrollers:YES];
		
		[self createOutlineView];
		
		_contentView = [[CPSplitView alloc] initWithFrame:CGRectMake(0, 0, CGRectGetWidth([_splitVertical bounds]) - 300, CGRectGetHeight([_splitVertical bounds]))];
		[_contentView setVertical:NO];
		[_contentView setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable];
		
		[_splitVertical addSubview:_navigationArea];
		[_splitVertical addSubview:_contentView];
		
		_detailArea = [[CPScrollView alloc] initWithFrame:CGRectMake(0, 0, CGRectGetWidth([_contentView bounds]), 500)];
		[_detailArea setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable ];
		[_detailArea setAutohidesScrollers:YES];
		
		[self createDetailTableView];
		
		_detailView = [[CPScrollView alloc] initWithFrame:CGRectMake(0, 0, CGRectGetWidth([_contentView bounds]), CGRectGetHeight([_contentView bounds]) - 500)];
		[_detailView setAutohidesScrollers:YES];
		
		[self createDetailOutlineView];
		
		[_contentView addSubview:_detailArea];
		[_contentView addSubview:_detailView];
	
		[self addSubview:_splitVertical];
	}
	
	return self;
}

-(void) createDetailOutlineView
{
	_detailOutlineView = [[CPOutlineView alloc] initWithFrame:[_detailView bounds]];
	[_detailOutlineView setRowHeight: 39];
	
	var typeColumn = [[CPTableColumn alloc] initWithIdentifier:@"TypeColumn"];
	[[typeColumn headerView] setStringValue:@"Type"];
	[typeColumn setWidth: 300];
	
	var imageColumnView = [[EAImageColumnView alloc] initWithFrame:CGRectMake(0, 0, [typeColumn width], [_detailOutlineView rowHeight])];
	[imageColumnView setImageView: [[CPImageView alloc] initWithFrame:CGRectMake(3, 3, 32, 32)]];
	[imageColumnView setTextField: [[CPTextField alloc] initWithFrame:CGRectMake(40, 10, 250, 20)]];
	[typeColumn setDataView:imageColumnView];
	
	var locationColumn = [[CPTableColumn alloc] initWithIdentifier:@"LocationColumn"];
	[[locationColumn headerView] setStringValue:@"Location"];
	[locationColumn setWidth: 300];
	
	var flagColumn = [[CPTableColumn alloc] initWithIdentifier:@"FlagColumn"];
	[[flagColumn headerView] setStringValue:@"Inventory Flag"];
	[flagColumn setWidth: 200];
	
	var quantityColumn = [[CPTableColumn alloc] initWithIdentifier:@"QuantityColumn"];
	[[quantityColumn headerView] setStringValue:@"Quantity"];
	[quantityColumn setWidth: 100];
	
	[_detailOutlineView addTableColumn:typeColumn];
	[_detailOutlineView addTableColumn:locationColumn];
	[_detailOutlineView addTableColumn:flagColumn];
	[_detailOutlineView addTableColumn:quantityColumn];
	[_detailOutlineView setOutlineTableColumn:typeColumn];
	
	[_detailView setDocumentView:_detailOutlineView];
	
	var dataSource =  [[EADetailOutlineViewDataSource alloc] initWithObject:_detailOutlineView receiveNotificationFrom:_detailTableView];
	[_detailOutlineView setDataSource:dataSource];
}

-(void) createDetailTableView
{
	_detailTableView = [[CPTableView alloc] initWithFrame:CGRectMakeZero()]; 
	[_detailTableView setUsesAlternatingRowBackgroundColors:YES];
	[_detailTableView setAutoresizingMask:CPViewWidthSizable | CPViewHeightSizable | CPViewMaxXMargin];
	[_detailTableView setRowHeight:64];
	
	var imageColumn = [[CPTableColumn alloc] initWithIdentifier:@"ImageColum"];
	[[imageColumn headerView] setStringValue:@"Icon"];
	[imageColumn setWidth: 64];
	[imageColumn setDataView:[[CPImageView alloc] initWithFrame:CGRectMake(0, 0, 64, 64)]];
	
	var nameColumn = [[CPTableColumn alloc] initWithIdentifier:@"NameColum"];
	[[nameColumn headerView] setStringValue:@"Name"];
	[nameColumn setWidth: 300];
	
	var priceColumn = [[CPTableColumn alloc] initWithIdentifier:@"BasePriceColum"];
	[[priceColumn headerView] setStringValue:@"Base Price"];
	[priceColumn setWidth: 200];
	
	var unitsAvailableColumn = [[CPTableColumn alloc] initWithIdentifier:@"UnitsAvailableColum"];
	[[unitsAvailableColumn headerView] setStringValue:@"Units Available"];
	[unitsAvailableColumn setWidth: 200];
	
	[_detailTableView addTableColumn:imageColumn];
	[_detailTableView addTableColumn:nameColumn];
	[_detailTableView addTableColumn:priceColumn];
	[_detailTableView addTableColumn:unitsAvailableColumn];
	[_detailArea setDocumentView:_detailTableView];
	
	var dataSource =  [[EADetailTableViewDataSource alloc] initWithObject:_detailTableView receiveNotificationFrom:_outlineView];
	[_detailTableView setDataSource:dataSource];
}

-(void) createOutlineView
{	
	_outlineView = [[CPOutlineView alloc] initWithFrame:[_navigationArea bounds]];
	[_outlineView setHeaderView:nil];
	[_outlineView setCornerView:nil];
	
	var column = [[CPTableColumn alloc] initWithIdentifier:@"marketGroupColumn"];
	[column setWidth: 280];
	[column setDataView:[[EAImageColumnView alloc] initWithFrame:CGRectMake(0, 0, [column width], [_outlineView rowHeight])]];
	
	[_outlineView addTableColumn:column];
	[_outlineView setOutlineTableColumn:column];
	
	[_navigationArea setDocumentView:_outlineView];
	
	var dataSource = [[EAMarketGroupOutlineDataSource alloc] init];
	[_outlineView setDataSource:dataSource];
}
@end

/* =============================================== */
/* = OutlineView Column With Image and TextField = */
/* =============================================== */

@implementation EAImageColumnView : CPView
{
	CPImageView		_imageView;
	CPTextField		_textField;
}

-(void) setImageView:(CPImageView)view
{
	[self replaceSubview:_imageView with:view];
	_imageView = view;
}

-(void) setTextField:(CPTextField)textField
{
	[self replaceSubview:_textField with:textField];
	_textField = textField;
}

-(id) initWithFrame:(CGRect)aFrame
{
	self = [super initWithFrame:aFrame];
	
	if(self)
	{
		
		
		_imageView 	= [[CPImageView alloc] initWithFrame:CGRectMake(3, 3, 16, 16)];
		_textField	= [[CPTextField alloc] initWithFrame:CGRectMake(20, 2, 250, 20)];
		
		[self addSubview: _imageView];
		[self addSubview: _textField];
	}
	
	return self;
}

-(void) setObjectValue:(id)anObject
{
	var image = [[anObject objectForKey:@"lookupTable"] objectForKey:[anObject objectForKey:@"image"]];
	
	[_imageView setImage: image];
	[_textField setStringValue:[anObject objectForKey:@"string"]];
}

-(id) initWithCoder:(CPCoder)aCoder
{
	self = [super initWithCoder:aCoder];
	
	if(self)
	{
		_imageView 	= [aCoder decodeObjectForKey:@"_imageView"];
		_textField 	= [aCoder decodeObjectForKey:@"_textField"];
	}
	
	return self;
}

-(void) encodeWithCoder:(CPCoder)aCoder
{
	[super encodeWithCoder:aCoder];

	[aCoder encodeObject:_imageView forKey:@"_imageView"];
	[aCoder encodeObject:_textField forKey:@"_textField"];
}
@end

/* ================================ */
/* = DetailOutlineView DataSource = */
/* ================================ */

@implementation EADetailOutlineViewDataSource : CPObject
{
	CPData 			_data;
	CPOutlineView 	_outlineView;
}

-(id) initWithObject:(CPOutlineView)outlineView receiveNotificationFrom:(CPTableView)tableView
{
	self = [super init];
	
	_data = nil;
	_outlineView = outlineView;
	
	[[CPNotificationCenter defaultCenter]
	        addObserver:self
	        selector:@selector(tableViewSelectionDidChange:)
	        name:CPTableViewSelectionDidChangeNotification
	        object:tableView];
	
	
	return self;
}

-(void) setData:(CPData)data
{
	_data = data;
	[_outlineView reloadData];
}

-(void) connection:(CPURLConnection)aConnection didReceiveData:(CPString)data
{
	_data = [CPData dataWithJSONObject:JSON.parse(data)];
	[_outlineView reloadData];
}

-(void) tableViewSelectionDidChange:(CPNotification)notification
{
	var tableView 		= [notification object];
	var selectedRow 	= [[tableView selectedRowIndexes] firstIndex];
	var item 			= [[tableView dataSource] data];
	
	if (selectedRow != -1)
	{
		var request 	= [CPURLRequest requestWithURL:_getTreeForTypeIDURL + [item JSONObject][selectedRow].pk];
		var connection	= [CPURLConnection connectionWithRequest:request delegate:self];
	}
}

-(id) outlineView:(CPOutlineView)outlineView child:(int)index ofItem:(id)item
{
	if(item)
	{
		return [CPData dataWithJSONObject: [item JSONObject].childs[index]];
	}
	
	else
	{
		return [CPData dataWithJSONObject: [_data JSONObject].childs[index]];
	}
}

-(BOOL) outlineView:(CPOutlineView)outlineView isItemExpandable:(id)item
{
	if ([item JSONObject].childs.length > 0)
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
	if(item)
	{
		return [item JSONObject].childs.length;
	}
	
	else
	{
		if (_data)
		{
			return [_data JSONObject].childs.length;
		}
	
		else
		{
			return 0;
		}
	}
}

-(id)outlineView:(CPOutlineView)outlineView objectValueForTableColumn:(CPTableColumn)tableColumn byItem:(id)item
{	
	if ([tableColumn identifier] == @"TypeColumn")
	{
		//return [item JSONObject].data.typeName;
		
		if ([_eveTypeIconsDictionary objectForKey:[item JSONObject].data.invTypeID] == nil)
		{
			var category = [item JSONObject].categoryName;
			var subDir = @"/";
			var fileExtension = @".png";

			switch(category)
			{
				case "Deployable":
					subDir = @"/deployabletypes_png/64_64/";
					break;

				case "Drone":
					subDir = @"/dronetypes_png/64_64/";
					break;

				case "Entity":
					subDir = @"/entitytypes_png/64_64/";
					break;

				case "Planetary Interaction":
					subDir = @"/planetaryinteractiontypes_png/64_64/";
					break;

				case "Ship":
					subDir = @"/shiptypes_png/128_128/";
					break;

				case "Sovereignty Structures":
					subDir = @"/sovereigntystructurestypes_png/64_64/";
					break;

				case "Station":
					subDir = @"/stationtypes_png/64_64/";
					break;

				case "Structure": 
					subDir = @"/structuretypes_png/64_64/";
					break;

				default:
					fileExtension = @"_64.png";
					break;
			}

			var image = [[CPImage alloc] initWithContentsOfFile:_eveTypesIconsURL + subDir + [item JSONObject].data.invTypeID + fileExtension];
			[_eveTypeIconsDictionary setObject:image forKey:[item JSONObject].data.invTypeID];
			
			return [CPDictionary dictionaryWithObjects:[_eveTypeIconsDictionary, [item JSONObject].data.invTypeID, [item JSONObject].data.typeName] forKeys:[@"lookupTable", @"image", @"string"]];
		}

		else
		{
			return [CPDictionary dictionaryWithObjects:[_eveTypeIconsDictionary, [item JSONObject].data.invTypeID, [item JSONObject].data.typeName] forKeys:[@"lookupTable", @"image", @"string"]];
		}

	}

	if ([tableColumn identifier] == @"LocationColumn")
	{
		return [item JSONObject].data.location;
	}
	
	if ([tableColumn identifier] == @"FlagColumn")
	{
		return [item JSONObject].data.flag;
	}
	
	if ([tableColumn identifier] == @"QuantityColumn")
	{
		return [item JSONObject].data.quantity;
	}
	
	//return [item JSONObject].data.typeName;
}

@end

/* ============================ */
/* = Detail Table Data Source = */
/* ============================ */

@implementation EADetailTableViewDataSource : CPObject
{
	CPData 			_data;
	CPTableView 	_tableView;
}

-(id) initWithObject:(CPTableView)tableView receiveNotificationFrom:(CPOutlineView)outlineView
{
	self = [super init];
	
	_data = [CPData dataWithJSONObject:[]];
	_tableView = tableView;
	
	[[CPNotificationCenter defaultCenter]
	        addObserver:self
	        selector:@selector(outlineViewSelectionDidChange:)
	        name:CPOutlineViewSelectionDidChangeNotification
	        object:outlineView];
	
	
	return self;
}

-(void) outlineViewSelectionDidChange:(CPNotification)notification
{
	var outlineView 	= [notification object];
	var selectedRow 	= [[outlineView selectedRowIndexes] firstIndex];
	var item 			= [outlineView itemAtRow:selectedRow];
	
	
	if ([item JSONObject].fields.hasTypes)
	{
		var request			= [CPURLRequest requestWithURL:_listCorpAssetsURL + [item JSONObject].pk];
		var connection		= [CPURLConnection connectionWithRequest:request delegate:self];
	}
	
	else 
	{
		_data = [CPData dataWithJSONObject:[]];
		[_tableView reloadData];
		[_tableView deselectAll];
		
		/* ================================= */
		/* = climing up the View hirarchie = */
		/* ================================= */
		[[[[[[[[_tableView superview] superview] superview] superview] superview] detailOutlineView] dataSource] setData:nil];
	}
}

-(CPData) data
{
	return _data;
}

-(void) setData:(CPData)data
{
	_data = data;
	[_tableView reloadData];
	[_tableView deselectAll];
	
	[[[[[[[[_tableView superview] superview] superview] superview] superview] detailOutlineView] dataSource] setData:nil];
}

-(void) connection:(CPURLConnection)aConnection didReceiveData:(CPString)data
{
	_data = [CPData dataWithJSONObject:JSON.parse(data)];
	[_tableView reloadData];
	[_tableView deselectAll];
	
	/* ================================= */
	/* = climing up the View hirarchie = */
	/* ================================= */
	[[[[[[[[_tableView superview] superview] superview] superview] superview] detailOutlineView] dataSource] setData:nil];
}

-(int) numberOfRowsInTableView:(CPTableView)aTableView
{
	return [_data JSONObject].length;
}

-(id) tableView:(CPTableView)aTableView objectValueForTableColumn:(CPTableColumn)aColumn row:(int)aRowIndex
{
	var anObject = [CPData dataWithJSONObject:[_data JSONObject][aRowIndex]];

	if([aColumn identifier] == @"ImageColum")
	{
		if ([_eveTypeIconsDictionary objectForKey:[anObject JSONObject].pk] == nil)
		{
		
			var category = [anObject JSONObject].fields.groupID.fields.categoryID.fields.categoryName;
			var subDir = @"/";
			var fileExtension = @".png";
		
			switch(category)
			{
				case "Deployable":
					subDir = @"/deployabletypes_png/64_64/";
					break;
			
				case "Drone":
					subDir = @"/dronetypes_png/64_64/";
					break;
			
				case "Entity":
					subDir = @"/entitytypes_png/64_64/";
					break;
			
				case "Planetary Interaction":
					subDir = @"/planetaryinteractiontypes_png/64_64/";
					break;
			
				case "Ship":
					subDir = @"/shiptypes_png/128_128/";
					break;
			
				case "Sovereignty Structures":
					subDir = @"/sovereigntystructurestypes_png/64_64/";
					break;
			
				case "Station":
					subDir = @"/stationtypes_png/64_64/";
					break;
			
				case "Structure": 
					subDir = @"/structuretypes_png/64_64/";
					break;
			
				default:
					fileExtension = @"_64.png";
					break;
			}
		
			var image = [[CPImage alloc] initWithContentsOfFile:_eveTypesIconsURL + subDir + [anObject JSONObject].pk + fileExtension];
			[_eveTypeIconsDictionary setObject:image forKey:[anObject JSONObject].pk];
			return image;
		}
	
		else
		{
			var image = [_eveTypeIconsDictionary objectForKey:[anObject JSONObject].pk];
			return image;	
		}
	}
	
	if([aColumn identifier] == @"NameColum")
	{
		return [anObject JSONObject].fields.typeName;
	}
	
	if([aColumn identifier] == @"BasePriceColum")
	{
		return [anObject JSONObject].fields.basePrice);
	}

	if([aColumn identifier] == @"UnitsAvailableColum")
	{
		return [anObject JSONObject].extras.units_available;
	}
}

@end

/* ================================= */
/* = MArketGroupOutline DataSource = */
/* ================================= */

@implementation EAMarketGroupOutlineDataSource : CPObject
{

}

-(id) init
{
	self = [super init];
	return self;
}

-(id) outlineView:(CPOutlineView)outlineView child:(int)index ofItem:(id)item
{
	if (item == nil)
	{
		var _data = [_marketGroupsDictionary objectForKey:@"root"];
		return [CPData dataWithJSONObject:[_data JSONObject][index]];
	}

	else
	{
		var _data = [_marketGroupsDictionary objectForKey:[item JSONObject].pk];
		return [CPData dataWithJSONObject:[_data JSONObject][index]];
	}
}

-(BOOL) outlineView:(CPOutlineView)outlineView isItemExpandable:(id)item
{
	return ![item JSONObject].fields.hasTypes;
}

-(int) outlineView:(CPOutlineView)outlineView numberOfChildrenOfItem:(id)item
{
	if(item == nil)
	{
		if ([_marketGroupsDictionary objectForKey:@"root"] == nil)
		{
			var controller		= [EAAsyncMarketGroupController controllerWithOutlineView:outlineView forItem:item];
			var request			= [CPURLRequest requestWithURL:_marketGroupsURL];
			var connection		= [CPURLConnection connectionWithRequest:request delegate:controller];
			
			return 0;
		}
		
		else
		{
			return [[_marketGroupsDictionary objectForKey:@"root"] JSONObject].length;
		}
	}
	
	else
	{
		if([_marketGroupsDictionary objectForKey:[item JSONObject].pk] == nil)
		{
			var controller		= [EAAsyncMarketGroupController controllerWithOutlineView:outlineView forItem:item];
			var request			= [CPURLRequest requestWithURL:_marketGroupsURL + [item JSONObject].pk];
			var connection		= [CPURLConnection connectionWithRequest:request delegate:controller];
			
			return 0;
		}
		
		else 
		{
			return [[_marketGroupsDictionary objectForKey:[item JSONObject].pk] JSONObject].length;
		}
	}
}

-(id)outlineView:(CPOutlineView)outlineView objectValueForTableColumn:(CPTableColumn)tableColumn byItem:(id)item
{	
	var string 	= [item JSONObject].fields.marketGroupName;
	var image 	= nil;
	
	if ([item JSONObject].fields.iconID == nil)
	{
		if ([_eveSmallIconsDictionary objectForKey:@"default"] == nil)
		{
			var image = [[CPImage alloc] initWithContentsOfFile:_eveDefaultIconURL];
			[_eveSmallIconsDictionary setObject:image forKey:@"default"];
		}
		
		image = @"default";
	}
	
	else
	{
		if ([_eveSmallIconsDictionary objectForKey:[item JSONObject].fields.iconID.pk] == nil)
		{
			var image =  [[CPImage alloc] initWithContentsOfFile:_eveSmallIconsURL + [item JSONObject].fields.iconID.fields.iconFile + @".png"];
			[_eveSmallIconsDictionary setObject:image forKey:[item JSONObject].fields.iconID.pk];
		}
		
		image = [item JSONObject].fields.iconID.pk;
	}
	
	return [CPDictionary dictionaryWithObjects:[_eveSmallIconsDictionary, image, string] forKeys:[@"lookupTable", @"image", @"string"]];
}

@end 

/* ========================================== */
/* = Async Controller for OutlineDataSource = */
/* ========================================== */

@implementation EAAsyncMarketGroupController : CPObject
{
	CPOutlineView					_outlineView;
	id								_item;	
}

-(id) initWithOutlineView:(CPOutlineView)outlineView forItem:(id)item
{
	self = [super init];
	
	if (self)
	{
		_outlineView 	= outlineView;
		_item 			= item;
	}
	
	return self;
}

-(void)connection:(CPURLConnection)aConnection didReceiveData:(CPString)data
{
	var _data = [CPData dataWithJSONObject:JSON.parse(data)];

	if (_item == nil)
	{
		[_marketGroupsDictionary setObject:_data forKey:@"root"];
	}
	
	else
	{
		[_marketGroupsDictionary setObject:_data forKey:[_item JSONObject].pk];
	}
	
	[_outlineView reloadItem:_item reloadChildren:YES];	
}

+(id) controllerWithOutlineView:(CPOutlineView)outlineView forItem:(id)item
{
	return [[EAAsyncMarketGroupController alloc] initWithOutlineView:outlineView forItem:item];
}
@end