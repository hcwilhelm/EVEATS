// 
//  EVProgressView.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-06-12.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 

@import <Foundation/Foundation.j>
@import "../Utils/BackendURLS.j"

var EVProgressViewStatusPending   = 1 << 0;
var EVProgressViewStatusProgress  = 1 << 1;
var EVProgressViewStatusSuccess   = 1 << 2;

@implementation EVProgressView : CPView
{
  CPProgressIndicator _progressIndicator;
  
  CPURLRequest        _progressRequest;
  CPURLConnection     _progressConnection;
  
  int                 _status;
  String              _taskID; 
  int                 _requestIntervall;
}

-(id) initWithFrame:(CPRect)aFrame forTaskID:(String)aID
{
  self = [super initWithFrame:aFrame];
  
  if (self)
  {
    var centerX = aFrame.size.width / 2.0;
    var centerY = aFrame.size.height / 2.0;
    
    _progressIndicator = [[CPProgressIndicator alloc] initWithFrame:CGRectMake(centerX - 128, centerY - 8, 256, 16)];
    [_progressIndicator setAutoresizingMask:  CPViewMinXMargin | CPViewMaxXMargin | CPViewMinYMargin | CPViewMaxYMargin];
    [_progressIndicator setStyle:CPProgressIndicatorBarStyle];
    [_progressIndicator setMinValue: 0.0];
    [_progressIndicator setMaxValue: 100.0];
    [_progressIndicator setDoubleValue: 0.0];
    
    [self addSubview: _progressIndicator];
    
    _status = EVProgressViewStatusPending;
    _taskID = aID;
    _requestIntervall = 100;
    
    _request = [CPURLRequest requestWithURL:baseURL + "/tasks/" + _taskID + "/status"];
    _progressConnection = [CPURLConnection connectionWithRequest:_request delegate:self];
  }
  
  return self;
}

-(Boolean) isPending
{
  if (_status == EVProgressViewStatusPending)
  {
    return YES;
  }
  
  else
  {
    return NO;
  }
}

-(Boolean) isInProgress
{
  if (_status == EVProgressViewStatusProgress)
  {
    return YES;
  }
  
  else
  {
    return NO;
  }
}

-(Boolean) isSuccess
{
  if (_status == EVProgressViewStatusSuccess)
  {
    return YES;
  }
  
  else
  {
    return NO;
  }
}

-(void) connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  if (connection == _progressConnection)
  {
    json = CPJSObjectCreateWithJSON(data);
    
    if (json.task.status == "PENDING")
    {
      _status = EVProgressViewStatusPending;
      
      window.setTimeout(function() { 
          _progressConnection = [CPURLConnection connectionWithRequest:_request delegate:self];
        }, _requestIntervall);
    }
    
    if (json.task.status == "PROGRESS")
    {
      _status = EVProgressViewStatusProgress;
      
      var currentProgressValue = json.task.result.current;
      var maximumProgressValue = json.task.result.total;
      
      [_progressIndicator setDoubleValue: currentProgressValue / (maximumProgressValue / 100.0)];
      
      window.setTimeout(function() { 
          _progressConnection = [CPURLConnection connectionWithRequest:_request delegate:self];
        }, _requestIntervall);
    }
    
    if (json.task.status == "SUCCESS")
    {
      _status = EVProgressViewStatusSuccess;
      [_progressIndicator setDoubleValue: 100.0];
      
      [[CPNotificationCenter defaultCenter] postNotificationName:AppControllerCharChanged object:self];
    }
  }
}

@end