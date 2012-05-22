
@interface LoginController : NSWindowController
{
    IBOutlet NSImageView* eveIconView;
    IBOutlet NSTextField* registerEmailTextField;
    IBOutlet NSTextField* registerUsernameTextField;
    IBOutlet NSTextField* registerPasswordTextField;
    IBOutlet NSTextField* registerConfirmTextField;
    IBOutlet NSButton* registerButton;
    IBOutlet NSTextField* loginUsernameTextField;
    IBOutlet NSTextField* loginPasswordTextField;
    IBOutlet NSButton* loginButton;
    IBOutlet NSButton* postTestButton;
    IBOutlet NSTextField* messageTextField;
}
- (IBAction)login:(id)aSender;
- (IBAction)register:(id)aSender;
- (IBAction)sendPOST:(id)aSender;
@end