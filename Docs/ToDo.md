# To Do

## GenerateGridPoints

* Requires an advanced license, make a basic license version

## GenerateGrid

* If active annotation target has display turned off, preview does not show.
* There are unused methods in the form, Several classes have FIXMEs and the
  functionality feels incomplete.

## AddLength

* Make it work with geographic data, and remove warning.

## AddArea

* Make it work with geographic data, and remove warning.
* Alert user if over-writing data in an existing `Acres` field (applies to
  multiple tools).

## AddCoords

* Allow add XY for lines and polygons as well.
* If there are a lot of points, provide a progress bar.
* If data is in a compressed FGDB, it is read-only, therefore, it will not show
  up in the list of available features (this can be confusing).
* FormData class is incomplete, see FIXMEs.

## Random Select

* Counts features in all classes when loading the form.  This can take a long
  time (do something smarter).
* Use selection if provided.
* Toggle for with or without replacement.

## Obscure Points

* NIM bug, provide workaround

## Line To Rectangle

* See FIXMEs in code
