
@interface AssetsController : NSViewController
{
    IBOutlet NSView* navigationView;
    IBOutlet NSView* navigationFilterView;
    IBOutlet NSSplitView* navigationSplitView;
    IBOutlet NSView* navigationDataView;
    IBOutlet NSView* navigationMetaInfoView;
    IBOutlet NSView* navigationMetaInfoLabelView;
    IBOutlet CPButtonBar* navigationButtonBar;
    IBOutlet NSView* contentView;
    IBOutlet NSSplitView* contentSplitView;
}
- (IBAction)toggleMetaInfoView:(id)aSender;
@end