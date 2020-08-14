---
layout: project
title: RadBeacon-Configurator-Android
icon: icon-github
caption: An Android Java app to scan and batch-configure RadBeacon Dots BLE beacons.
date: 2020-08-05 13:10:46
image:
  path: /assets/gabryxx7/img/GitHub/RadBeacon-Configurator-Android/screenshot_list.jpg
description: An Android Java app to scan and batch-configure RadBeacon Dots BLE beacons.
links:
- title: Source
  url: https://github.com/Gabryxx7/RadBeacon-Configurator-Android

---

# Android RadBeacon Dots Configurator
A (not that) simple Android App to configure and **batch-configure** [RadBeacon Dots BLE proximity beacons](https://store.radiusnetworks.com/products/radbeacon-dot).

## Screenshots

<img src="/assets/gabryxx7/img/GitHub/RadBeacon-Configurator-Android/screenshot_list.jpg" height="400"> &nbsp; 
<img src="/assets/gabryxx7/img/GitHub/RadBeacon-Configurator-Android/screenshot_config.jpg" height="400"> &nbsp; 
<img src="/assets/gabryxx7/img/GitHub/RadBeacon-Configurator-Android/screenshot_batch.jpg" height="400">

## Features
- Scan for beacons
- Sort and filter the list of scanned beacons
- Read configurable properties
- Configure a beacon
- **Set up a batch configurator which automatically reads and configure all configurable beacons in range. Just hold that button to put the beacon in configuration mode and let the app do its job!**

## Structure

The app is made app of few main parts:
- `BLEScanner` service: This service runs on its own thread and constantly scans for bleutooth beacons, it can tell if the beacon is in configuration mode and automatically reads its data. Upon reading it, the beacon is ready to be configured
- `TrackerPreferences`: This class is a `SharedPreferences` wrapper and contains all the settings of the app
- `ScannedDeviceRecord`: This class contains the information about any scaned device (it could be used for non-beacons bluetooth devices too)
- The app uses [`greenrobot.EventBus`](https://github.com/greenrobot/EventBus), an incredible publish/subscribe event bus package for Android! It allows me to keep the code clean while managing multiple threads and classes and letting them communicate
