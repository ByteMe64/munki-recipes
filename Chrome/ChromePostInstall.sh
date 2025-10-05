<key>postinstall_script</key>
<string>
#!/bin/bash

# /Library/Managed Preferences/ is the location these settings should be.

# This script creates a managed preference file to configure Google Chrome's
# automatic update, relaunch, and branding behavior.

# --- UPDATE SETTINGS ---
# Key: UpdateDefault - Value: 1 (Allows updates)
defaults write com.google.Chrome UpdateDefault -int 1

# Key: AutoUpdateCheckPeriodMinutes - Value: 240 (Check for updates every 4 hours)
defaults write com.google.Chrome AutoUpdateCheckPeriodMinutes -int 240


# --- RELAUNCH SETTINGS ---
# Key: RelaunchNotification - Value: 2 (Forces a relaunch after the notification period)
defaults write com.google.Chrome RelaunchNotification -int 2

# Key: RelaunchNotificationPeriod - Value: 14400000 (Sets notification window to 4 hours in ms)
defaults write com.google.Chrome RelaunchNotificationPeriod -int 14400000


# --- BRANDING SETTINGS ---
# Set the homepage and startup page to your company's website
defaults write com.google.Chrome HomepageLocation -string "https://google.co.uk"
defaults write com.google.Chrome ShowHomeButton -bool true
defaults write com.google.Chrome RestoreOnStartup -int 4
defaults write com.google.Chrome RestoreOnStartupURLs -array "https://google.co.uk"

# Create a managed bookmarks folder
# This creates a folder named "Company Links" with two bookmarks inside
defaults write com.google.Chrome ManagedBookmarks -array \
  '{ "name" = "iCC Links"; "children" = ( { "name" = "Company Portal"; "url" = "https://ic-consult.atlassian.net/wiki/spaces/HOME/overview?mode=global"; }, { "name" = "IT Helpdesk"; "url" = "https://ic-consult.atlassian.net/servicedesk/customer/portal/22"; }, { "name" = "Timelog"; "url" = "https://login.timelog.com/"; }, { "name" = "HR Works"; "url" = "https://ssl10.hrworks.de/y/dashboard"; } ); }'


exit 0
</string>