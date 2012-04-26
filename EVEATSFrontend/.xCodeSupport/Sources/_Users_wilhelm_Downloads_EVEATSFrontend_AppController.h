
@interface AppController : NSObject
{
    IBOutlet NSWindow* theWindow;
}
- (IBAction)toggleMetaInfoView:(id)aSender;
- (IBAction)toolbarItemManageAccoutClicked:(id)aSender;
- (IBAction)toolbarItemAssetsClicked:(id)aSender;
- (IBAction)charChanged:(id)aSender;
@end