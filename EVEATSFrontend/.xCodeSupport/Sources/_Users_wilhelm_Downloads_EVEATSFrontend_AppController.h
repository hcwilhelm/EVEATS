
@interface AppController : NSObject
{
    IBOutlet NSWindow* theWindow;
}
- (IBAction)toolbarItemManageAccoutClicked:(id)aSender;
- (IBAction)toolbarItemAssetsClicked:(id)aSender;
- (IBAction)charChanged:(id)aSender;
@end