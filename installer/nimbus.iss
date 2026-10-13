; Script de Instalacao do Navegador Nimbus via Inno Setup
#ifndef MyAppVersion
#define MyAppVersion "0.0.0-dev"
#endif
#define MyAppName "Navegador Nimbus"
#define MyAppPublisher "Nimbus"
#define MyAppURL "https://github.com/tgferr/nimbusbrowser"
#define MyAppExeName "Nimbus.exe"

[Setup]
AppId={{C6B8D1B4-4B4B-4E65-8E1A-8E28B02B5912}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
SourceDir=..
OutputDir=dist-installer
OutputBaseFilename=Nimbus-Setup-v{#MyAppVersion}
SetupIconFile=assets\nimbus_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Nimbus\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
