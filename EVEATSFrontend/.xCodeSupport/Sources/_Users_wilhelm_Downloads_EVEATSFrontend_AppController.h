
@interface AppController : NSObject
{
    IBOutlet NSWindow* theWindow;
    IBOutlet NSSplitView* verticalSplitView;
    IBOutlet NSView* filterView;
    IBOutlet NSView* infoLabelView;
    IBOutlet CPButtonBar* leftButtonBar;
}

@end