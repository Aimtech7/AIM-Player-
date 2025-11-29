; Inno Setup Script
[Setup]
AppName=AIM PLAYER
AppVersion=1.0
DefaultDirName={pf}\AIM PLAYER
DefaultGroupName=AIM PLAYER
OutputBaseFilename=AIM_PLAYER_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AIM PLAYER"; Filename: "{app}\app.exe"
