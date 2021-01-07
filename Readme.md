# Alaska Pak

The National Park Service AlaskaPak is a collection of custom tools developed
to meet the needs of GIS users in the Alaska Region. This toolkit is designed
to augment the functionality of esri’s ArcGIS by providing a simple interface
for many common tasks and workflows performed by GIS specialists, resource
managers, and other scientists working with spatial data at NPS.

This repo contains A MS Visual Studio solution with two projects:

1) AlaskaPak -- An ArcGIS 10.x Add-In written in C#, .NET Framework 4.5,
   ArcObjects 10.x, and WinForms. See the
   [Config](./AlaskaPak/Config.esriaddinx) file for a list of tools provided in
   the Add-In.

2) ConfigurationEditor -- A windows App, written in C#, .NET Framework 3.5,
   and WPF.  Used to allow user's to change the paths embedded in the
   AlaskaPak Add-In, after it has been deployed.

Many of the tools in the Add-In are ArcGIS GeoProcessing (GP) tools (python
scripts) in an esri toolbox.  This toolbox is required for the Add-In to work
but the toolbox, and/or individual tools can be deployed without the Add-In if
desired.  The toolbox and tools are in the `GPTools` folder.

## Build

* Clone this repository to your local file system.
* Confirm that the [PathToToolBox](./AlaskaPak/PathToToolBox.txt) and
[PathToThemeManager](./AlaskaPak/PathToThemeManager.txt) have the correct
paths to the locations where you will be installing the Alaska Pak toolbox
and [Theme Manager](https://github.com/AKROGIS/ThemeManager).  These should
be stable locations accessible to ArcGIS and those who will be using the tools.
* Install the version of Microsoft Visual Studio Community supported by your
version of ArcGIS.
* Install the ArcObjects SDK (comes with ArcGIS Desktop 10.x).
* Open `AlaskaPak.sln` in Visual Studio.
* Select `Build -> Build Solution` from the Visual Studio menu.

## Deploy

### For Personal Use

* Build a release version
* Copy the toolbox folder (`GPTools`) to the path in
[PathToToolBox](./AlaskaPak/PathToToolBox.txt).
* (Optional) Install [Theme Manager](https://github.com/AKROGIS/ThemeManager)
  to the path in [PathToThemeManager](./AlaskaPak/PathToThemeManager.txt).
* Double click the file `AlaskaPak/bin/release/AlaskaPak3.esriAddIn` to
  invoke the esri Add-In installer.

### For Organizational Use

* Before building, make sure that the
  [Path To ToolBox](./AlaskaPak/PathToToolBox.txt), and the path to
  [Theme Manager](https://github.com/AKROGIS/ThemeManager) are network
  locations accessible to all organizational users.
* Build
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

* Build a release version
* Create a deployment folder with the name and version
* Copy the file `AlaskaPak/bin/release/AlaskaPak3.esriAddIn` to the deployment
  folder.
* Copy the `ConfigurationEditor/bin/releaseConfigurationEditor.exe` to the
  deployment folder.
* Copy the `GPTools` folder to to the deployment folder.
* Zip up deployment folder.
* Distribute (i.e. <https://irma.nps.gov/DataStore/Reference/Profile/2176910>)

## Using

If necessary, see the detailed
[installation instructions](./Docs/AlaskaPakV3_Installation.docx)
to activate the AlaskaPak toolbar in ArcMap.

There is a help option in the menu on the toolbar, as well as help with
individual tools once activated.

The scripts in the toolbox folder can be run from the command line or in the
ArcMap python window.  See the individual script files for details on usage.

Most tools require only an ArcView (basic) license, however some tools
require a more advanced license.  See
[License Requirements](./Docs/License Level Requirements.txt)
for details.
