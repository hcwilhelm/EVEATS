class AccountOperationResult():
    Success         = False
    ErrorCode       = 999
    Message    = ""

    def __init__(self, Success=True, ErrorCode=999, Message=""):
        if(Success):
            self.Success = True
            self.ErrorCode = 0
            if (Message == ""): Message = "Success"
            self.Message = Message
        else:
            self.Success = False
            self.ErrorCode = ErrorCode
            if (Message == ""): Message = "No message given"
            self.Message = Message

    def __str__(self):
        return '{"Success":%s, "ErrorCode":%d, "Message":"%s"}' % (str(self.Success).lower(), self.ErrorCode, self.Message)