
@interface UserController : NSViewController
{
    IBOutlet NSTextField* usernameTextField;
    IBOutlet NSTextField* emailTextField;
    IBOutlet NSTextField* passwordTextField;
    IBOutlet NSTextField* confirmTextField;
    IBOutlet NSTableView* apiKeyTableView;
    IBOutlet CPButtonBar* buttonBar;
    IBOutlet NSPopover* addAPIKeyPopover;
    IBOutlet NSTextField* keyIDTextField;
    IBOutlet NSTextField* vCodeTextField;
    IBOutlet NSTextField* nameTextField;
    IBOutlet NSButton* addApiKeyButton;
    IBOutlet NSButton* cancelButton;
}
- (IBAction)addKeyPopover:(id)aSender;
- (IBAction)addKey:(id)aSender;
- (IBAction)closeWindow:(id)aSender;
@end