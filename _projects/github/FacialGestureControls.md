---
layout: project
title: FacialGestureControls
icon: icon-github
caption: Windows control through facial gestures and emotion recognition. You can
  now act surprised when caught on stack overflow and boom your work windows are back
  on top. Raise or Lower the volume with your eyebrows, take a screenshot with a smile
  or send a message with a kiss.
date: 2019-04-23 10:47:26
image:
  path: /assets/gabryxx7/img/GitHub/FacialGestureControls/Start.png
description: Windows control through facial gestures and emotion recognition. You
  can now act surprised when caught on stack overflow and boom your work windows are
  back on top. Raise or Lower the volume with your eyebrows, take a screenshot with
  a smile or send a message with a kiss.
links:
- title: Source
  url: https://github.com/Gabryxx7/FacialGestureControls

---

# Expresso - Windows control with facial gestures
***Disclaimer**: I made this project more than 1 year ago and since then I haven't really touched it. I will tr to update this Readme to include more info about the project*

This is a little fun project developed as a final assignment for the course [INFO90003 - Designing Novel Interaction](https://handbook.unimelb.edu.au/2018/subjects/info90003)
at the University of Melbourne.

The project uses [Affectiva](https://www.affectiva.com/) to detect facial expressions and emojis in real time. The app has been recently updated to get video feed from file and process every frame in it.


# How to use it
There should be a release in the repository but if there is not, you'll find the pre-compiled exe in the `AffectivaWPF/bin/x64/Release` folder.

Once started you should be greeted with this window:


![Start](/assets/gabryxx7/img/GitHub/FacialGestureControls/Start.png)


## Camera Feed
The camera feed should look something like this:

![Main Window](/assets/gabryxx7/img/GitHub/FacialGestureControls/main1.png)

# Features and facial expressions
There are three categories of expressions:

| Seven Basic Emotions                                               | Action Units                                                                                                                                                                                                                                                                                                                                                                                                                  | Other                 |
|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| Contempt<br>Surprise<br>Anger<br>Sadness<br>Disgust<br>Fear<br>Joy | Scream<br>Flushed<br>Stuck Out Tongue<br>Wink<br>Smirk<br>Rage<br>Disappointed<br>Kissing<br>Laughing<br>Smiley<br>Relaxed<br>Brow Raise<br>Brow Furrow<br>Nose Wrinkle<br>Upper Lip Raise<br>Lip Corner Depress<br>Chin Raise<br>Lip Pucker<br>Lip Press<br>Lip Suck<br>Mouth Open<br>Eye Closure<br>Eye Widen<br>Cheek Raise<br>Lid Tighten<br>Dimpler<br>Lip Stretch<br>Jaw Drop<br>Inner Brow Raise<br>Smile<br>Attention | Engagement<br>Valence |

There are currently 14 actions registered in the app, implemented with the help of Windows Hooks in .NET and the `user32.dll` library.
I tried to keep the code modular so that new actions could be hooked up easily. The class `AffectivaActions` is where these actions are added to the list:
```cs        
private AffectivaActions()
{
      actionsFunction.Add("BrightnessDown", (handle, param1, param2) =>
      {
          Console.WriteLine("BRIGHTNESS DOWN");
          HookActions.BrightnessDown(handle);
          return true;
      });
      
      actionsFunction.Add("BrightnessUp", (handle, param1, param2) =>
      {
          Console.WriteLine("BRIGHTNESS UP");
          HookActions.BrightnessUp(handle);
          return true;
      });
...
}
```

Adding new actions is as easy as adding a tuple (ActionName, CallbackMethod) to the `actionsFunction` list.

The Affectiva features added in a similar way where each feature has a Type (Emoji, Emotion, Expression) an ID and a DisplayName. The empty strings below would become the name of the action to be performed when triggered. In order to trigger an action a feature as two values that need to be met:
- Threshold (default=50)
- Time (default 1)
An action gets triggered when the feature strength is over Threshold for Time seconds so in this example if Affectiva detects BrowseUp with an accuracy of over 50 for 1 second its correspondign action will be executed.  

```cs
...

featuresActions.Add(new AffectivaFeature(AffectivaFeature.FeatureType.Emoji,"scream", "Scream", "", 50, 1));
featuresActions.Add(new AffectivaFeature(AffectivaFeature.FeatureType.Emoji,"flushed", "Flushed", "", 50, 1));
featuresActions.Add(new AffectivaFeature(AffectivaFeature.FeatureType.Emoji,"stuckOutTongue", "StuckOutTongue", "", 50, 1));
featuresActions.Add(new AffectivaFeature(AffectivaFeature.FeatureType.Emoji,"stuckOutTongueWinkingEye", "StuckOutTongueWinkingEye", "", 50, 1));
featuresActions.Add(new AffectivaFeature(AffectivaFeature.FeatureType.Emoji,"wink", "Wink", "", 50, 1));
...

```
![Features](/assets/gabryxx7/img/GitHub/FacialGestureControls/features.png)


# Screenshot 
![Screenshot](/assets/gabryxx7/img/GitHub/FacialGestureControls/Screenshot1.jpg)

# YouTube Presentation
[Youtube Link](https://www.youtube.com/watch?v=fw9QCx4QEHs)
[![Video](/assets/gabryxx7/img/GitHub/FacialGestureControls/0.jpg)](https://www.youtube.com/watch?v=fw9QCx4QEHs)

