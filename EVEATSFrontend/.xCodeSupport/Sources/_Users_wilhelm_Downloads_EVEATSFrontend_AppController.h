
@interface AppController : NSObject
{
    IBOutlet NSWindow* theWindow;
    IBOutlet NSSplitView* splitViewMain;
    IBOutlet NSView* navigationArea;
    IBOutlet NSView* filterView;
    IBOutlet NSSplitView* navigationSplitView;
    IBOutlet NSView* dataView;
    IBOutlet NSView* metaInfoView;
    IBOutlet NSView* metaInfoLabelView;
    IBOutlet CPButtonBar* navigationAreaButtonBar;
    IBOutlet NSView* contentView;
}
- (IBAction)toggleMetaInfoView:(id)aSender;
- (IBAction)toolbarItemManageAccoutClicked:(id)aSender;
- (IBAction)toolbarItemAssetsClicked:(id)aSender;
- (IBAction)charChanged:(id)aSender;
@end