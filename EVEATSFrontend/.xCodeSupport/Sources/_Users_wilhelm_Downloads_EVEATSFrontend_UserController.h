
@interface UserController : NSViewController
{
    IBOutlet NSTextField* usernameTextField;
    IBOutlet NSTextField* emailTextField;
    IBOutlet NSTextField* passwordTextField;
    IBOutlet NSTextField* confirmTextField;
    IBOutlet NSTableView* apiKeyTableView;
    IBOutlet CPButtonBar* buttonBar;
}
- (IBAction)saveClicked:(id)aSender;
@end