KENTI MACROINVERTEBRADOS · version 0.5
======================================

Free program (MIT licence) for benthic macroinvertebrate data: automatic
family assignment, NOA BMWP', ASPT' and ABI, diversity, PCA and Excel report.
Source code: https://github.com/carlosmariaflores-cloud/kenti-macroinvertebrados


How to open it
--------------
1. Unzip this file into any folder (for example, the Desktop). Do not run it
   from inside the .zip.
2. Double-click "Kenti Macroinvertebrados.exe". It opens in its own window.
   Nothing needs to be installed.

The first time, Windows may show "Windows protected your PC" because the
program is not digitally signed: click "More info" and then "Run anyway".

Requirements: Windows 10 or 11 with Microsoft Edge (included with Windows) or
Google Chrome.

The interface opens in the language of the system. Use the ES / EN button at
the top right to switch; the choice is remembered.


How to use it
-------------
1. Copy your spreadsheet in Excel (first row: the sites; first column: the
   taxa) and paste it into cell A1 of tab 1. Totals, abundance % and similar
   summary columns are ignored automatically.
2. Check the Family column: blue, Kenti's proposal; amber, corrected spelling
   or a genus found in more than one family. To change it, type over it.
3. Tab 5, Biotic indices: BMWP', ASPT' and ABI by site, with their classes and
   the families without a score or completed with the Bolivian table.
4. "Export to Excel" saves the workbook in the data folder.

Score tables are built in: NOA BMWP' (Domínguez & Fernández 1998) completed
with the Bolivian BMWP/Bol for missing families (can be switched off), and ABI
(Prat et al. 2009). They can be replaced under "Score tables".


Where your data are
-------------------
Every change is saved automatically to:

    Documents\Kenti Macroinvertebrados\datos-macroinvertebrados.json

The same folder holds the backup, the exported Excel files and kenti.log.

To close the program, close its window.

Feedback and bugs: cmflores@csnat.unt.edu.ar (attach the .json and kenti.log).
