# Alaska Pak

The National Park Service AlaskaPak is a collection of custom tools developed
to meet the needs of GIS users in the Alaska Region. This toolkit is designed
to augment the functionality of esri’s ArcGIS by providing a simple interface
for many common tasks and workflows performed by GIS specialists, resource
managers, and other scientists working with spatial data at NPS.

This repo contains a Microsoft Visual Studio solution with two projects:

1) AlaskaPak -- An ArcGIS 10.x Add-In written in C#, .NET Framework 4.5,
   ArcObjects 10.x, and WinForms. The Add-In interface is an ArcMap toolbar.
   See the [Config](./AlaskaPak/Config.esriaddinx) file for a list of tools
   provided in the Add-In.

2) ConfigurationEditor -- A windows app, written in C#, .NET Framework 3.5,
   and WPF.  Used to allow user who download the tool from a distribution
   site like [IRMA](https://irma.nps.gov/DataStore/Reference/Profile/2176910)
   to change the paths embedded in the AlaskaPak Add-In.

Many of the tools in the Add-In are ArcGIS GeoProcessing (GP) tools (python
scripts) in an esri toolbox.  This toolbox is required for the Add-In to work.
However, the toolbox and/or individual tools can be deployed without the Add-In.
The toolbox and tools are in the `GPTools` folder.

## Build

* Clone this repository to your local file system.
* Confirm that the [PathToToolBox](./AlaskaPak/PathToToolBox.txt) and
[PathToThemeManager](./AlaskaPak/PathToThemeManager.txt) have the correct
paths to the locations where you will be installing the AlaskaPak toolbox
and [Theme Manager](https://github.com/AKROGIS/ThemeManager).  These should
be stable locations accessible to ArcGIS and those who will be using the tools.
* Install the version of Microsoft Visual Studio Community supported by your
version of ArcGIS.
* Install the ArcObjects SDK (comes with ArcGIS Desktop 10.x).
* Open `AlaskaPak.sln` in Visual Studio.
* Select `Build -> Build Solution` from the Visual Studio menu.

## Deploy

### For Personal Use

* Build a release version.
* Copy the toolbox folder (`GPTools`) to the path in
[PathToToolBox](./AlaskaPak/PathToToolBox.txt).
* (Optional) Install [Theme Manager](https://github.com/AKROGIS/ThemeManager)
  to the path in [PathToThemeManager](./AlaskaPak/PathToThemeManager.txt).
* Double click the file `AlaskaPak/bin/release/AlaskaPak3.esriAddIn` to
  invoke the esri Add-In installer.
* See the [installation instructions](./Docs/InstallationInstructions.md)
  if you need additional assistance.

### For Organizational Use

* Before building, make sure that the
  [Path To ToolBox](./AlaskaPak/PathToToolBox.txt), and the path to
  [Theme Manager](https://github.com/AKROGIS/ThemeManager) are network
  locations accessible to all organizational users.
* Build.
* Copy the toolbox folder (`GPTools`) to the path in
  [PathToToolBox](./AlaskaPak/PathToToolBox.txt).
* (Optional) Install [Theme Manager](https://github.com/AKROGIS/ThemeManager)
  to the path in [PathToThemeManager](./AlaskaPak/PathToThemeManager.txt).
* Copy the file `AlaskaPak/bin/release/AlaskaPak3.esriAddIn` to a network
  location for Add-Ins.  Users will need to specify this folder as their
  Add-In folder in the ArcMap Add-In Manager (menu
  `Customize -> Add-In Manager...`) in order for the Add-In to automatically
  load with ArcMap.

### For Public Distribution

* Build a release version.
* Create a deployment folder with the name and version (i.e. `AlaskaPak_v3.0`).
* Copy `AlaskaPak/bin/release/AlaskaPak3.esriAddIn` to the deployment folder.
* Copy `ConfigurationEditor/bin/releaseConfigurationEditor.exe` to the
  deployment folder.
* Copy the `GPTools` folder to to the deployment folder.
* Zip up deployment folder.
* Publish on the distribution site (i.e.
  [IRMA](https://irma.nps.gov/DataStore/Reference/Profile/2176910))
* If the [installation instructions](./Docs/InstallationInstructions.md)
  have changed, export them to PDF and upload to the distribution site.

## Using

If necessary, see the detailed
[installation instructions](./Docs/InstallationInstructions.md)
to activate the AlaskaPak toolbar in ArcMap.

There is a help option in the menu on the toolbar, as well as help with
individual GP tools in the toolbox interface.

The scripts in the toolbox folder can be run from the command line or in the
ArcMap python window.  See the individual script files for details on usage.

Each tool is registered with the ArcGIS customization system, so you can build
your own toolbar with just the tools you want. The GP tools can be used in your
own models and scripts just like any other GP tool.

Most tools require only an ArcView (basic) license, however some tools
require a more advanced license.  See
[License Requirements](./Docs/LicenseRequirements.md)
for details.

See the [To Do List](./Docs/ToDo.md) for a list of known issues.
