// 
//  EVProgressView.j
//  EVEATSFrontend
//  
//  Created by Hans Christian Wilhelm on 2012-06-12.
//  Copyright 2012 __MyCompanyName__. All rights reserved.
// 

@import <Foundation/Foundation.j>
@import "../Utils/BackendURLS.j"


// =================
// = Notifications =
// =================

ProgressViewDidFinish = @"ProgressViewDidFinish";

@implementation EVProgressView : CPView
{
  CPProgressIndicator _progressIndicator;
  
  CPURLRequest        _progressRequest;
  CPURLConnection     _progressConnection;
  
  boolean             running   @accessors(readonly);
  boolean             paused    @accessors;
  
  String              taskID    @accessors;
  int                 charID    @accessors;
  
  int                 timer     @accessors;
}

-(id) initWithFrame:(CPRect)aFrame forTaskID:(String)aTaskID andCharID:(int)aCharID
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
    
    running = NO;
    paused  = NO;
    
    taskID  = aTaskID;
    charID  = aCharID;
    
    timer   = 500;
  }
  
  return self;
}

-(void) start
{
  running = YES;
  
  _request = [CPURLRequest requestWithURL:baseURL + "/tasks/" + taskID + "/status"];
  _progressConnection = [CPURLConnection connectionWithRequest:_request delegate:self];
}

-(void) connection:(CPURLConnection)connection didReceiveData:(CPString)data
{
  if (connection == _progressConnection)
  {
    json = CPJSObjectCreateWithJSON(data);
    
    if (json.task.status == "PENDING")
    {
      window.setTimeout(function() { 
        _request = [CPURLRequest requestWithURL:baseURL + "/tasks/" + taskID + "/status"];
        _progressConnection = [CPURLConnection connectionWithRequest:_request delegate:self];
      }, timer);
    }
    
    if (json.task.status == "PROGRESS")
    { 
      var currentProgressValue = json.task.result.current;
      var maximumProgressValue = json.task.result.total;
      
      [_progressIndicator setDoubleValue: currentProgressValue / (maximumProgressValue / 100.0)];
      
      window.setTimeout(function() { 
        _request = [CPURLRequest requestWithURL:baseURL + "/tasks/" + taskID + "/status"];
        _progressConnection = [CPURLConnection connectionWithRequest:_request delegate:self];
      }, timer);
    }
    
    if (json.task.status == "SUCCESS")
    {
      console.log("Task success running NO");
      
      [_progressIndicator setDoubleValue: 100.0];
      running = NO;
      
      [[CPNotificationCenter defaultCenter] postNotificationName:ProgressViewDidFinish object:self];
    }
  }
}

@end