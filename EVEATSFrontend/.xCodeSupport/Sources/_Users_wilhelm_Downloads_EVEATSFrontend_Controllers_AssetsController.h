
@interface AssetsController : NSViewController
{
    IBOutlet NSView* navigationView;
    IBOutlet NSView* navigationFilterView;
    IBOutlet NSSearchField* searchField;
    IBOutlet NSSplitView* navigationSplitView;
    IBOutlet NSView* navigationDataView;
    IBOutlet NSView* navigationMetaInfoView;
    IBOutlet NSView* navigationMetaInfoLabelView;
    IBOutlet CPButtonBar* navigationButtonBar;
    IBOutlet NSView* contentView;
    IBOutlet NSSplitView* contentSplitView;
    IBOutlet NSView* assetView;
    IBOutlet NSView* asserDetailView;
    IBOutlet NSView* progressView;
    IBOutlet NSView* progressIndicator;
    IBOutlet NSTextField* progressTextField;
}
- (IBAction)toggleMetaInfoView:(id)aSender;
@end