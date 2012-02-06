
@interface UserController : NSObject
{
    IBOutlet NSPanel* loginPanel;
    IBOutlet NSImageView* loginLogoImageView;
    IBOutlet NSTextField* loginUserTextField;
    IBOutlet NSTextField* loginPasswordTextField;
    IBOutlet NSButton* loginButton;
    IBOutlet NSButton* loginRegisterButton;
    IBOutlet NSTextField* loginMessageTextField;
    IBOutlet NSPanel* registerPanel;
    IBOutlet NSImageView* registerLogoImageView;
    IBOutlet NSTextField* registerUserTextField;
    IBOutlet NSTextField* registerPasswordTextField;
    IBOutlet NSTextField* registerEmailTextField;
    IBOutlet NSButton* registerButton;
    IBOutlet NSButton* registerLoginButton;
    IBOutlet NSTextField* registerMessageTextField;
}
- (IBAction)loginPanelLogin:(id)aSender;
- (IBAction)loginPanelRegister:(id)aSender;
- (IBAction)registerPanelRegister:(id)aSender;
- (IBAction)registerPanelLogin:(id)aSender;
@end