# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).


## [Unreleased]

### Fixed

* Corrupted CFF index data

  there was a subtle bug in cff index implementation that resulted in
  a data corruption. in certain circumstances some items didn't get
  properly encoded. this happened when items were not previously accessed.

  this resulted, for instance, in missing glyphs. but only sometimes
  because indexes might've still contain data that shouldn't've been
  there. in combination with incorrect encoding (see further) this
  resulted in some glyphs still being rendered, sometimes even correctly.

  along with the fix a rather large api change landed. this resulted in
  quite a big diff.

  Alexander Mankuta

* Incorrect CFF encoding in subsets

  TTFunk used to reuse encoding from the original font. This mapping was
  incorrect for subset fonts which used not just a subset of glyphs but
  also a different encoding.

  A separate issue was that some fonts have empty CFF encoding. This
  incorrect mapping resulted in encoding that mapped all codes to glyph 0.

  This had impact on Prawn in particular. PDF spec explicitly says that
  CFF encoding is not to be used in OpenType fonts. `cmap` table should
  directly index charstrings in the CFF table. Despite this PDF renderers
  still use CFF encoding to retrieve glyphs. So TTFunk has to discard the
  original CFF encoding and supply its own.

  Alexander Mankuta

* `maxp` table

  The table is now correctly parsed and encoded for both TrueType and CFF-based
  OpenType fonts.

  Cameron Dutro, Alexander Mankuta

* Files are closed sooner

  Files were garbage collected but could stay open for longer than necessary.

  Jon Burgess

* Long date time in the `head` table

  The `created` and `modified` fields we parsed and encoded with incorrect
  endiannes. Additionally helper methods were added to convert these fields to
  and from Ruby `Time`.

   Jens Kutilek, Peter Goldstein

* Removed execution permissions on non-executable files

  Keenan Brock

### Changes

* Minimum Ruby is 2.7

  Alexander Mankuta

* Performance improvement in subsets construction

  Thomas Leitner

* CI improvememnts

  Peter Goldstein

## 1.7.0

### Changes

* Allow gem installation on Ruby 3.0

  Pavel Lobashov

* Allow TTC files to be read from IO object

  Tom de Grunt

## [1.6.2.1]

### Fixed

* 1.6.2 gem conains local debuging code. This is the same commit but without
  local changes.

  Alexander Mankuta

## [1.6.2]

### Fixed

* Reverted to pre 1.6 maxp table serialization.

  Cameron Dutro

## [1.6.1]

### Fixed

* Fixed maxp table encoding

  Cameron Dutro

## [1.6.0]

### Added

* OpenType fonts support

  * Added support for CFF-flavored fonts (also known as CID-keyed or OpenType fonts)
  * Added support for the VORG and DSIG tables
  * Improved charset encoding support
  * Improved font metrics calculations in the head, maxp, hhea, hmtx, and os/2 tables
  * Subsetted fonts verified with Font-Validator, fontlint, and Mac OS's Font Book

  Cameron Dutro

* Ruby 2.6 support

  Alexander Mankuta

* JRuby 9.2 support

  Alexander Mankuta

### Removed

* Dropped Ruby 2.1 & 2.2 support

  Alexander Mankuta

* Removed JRuby 9.1 support

  Alexander Mankuta

### Fixed

* Sort name table entries when generating subset font

  Matjaz Gregoric

* Map the 0xFFFF char code to glyph 0 in cmap format 4

  Matjaz Gregoric

* Order tables by tag when generating font subset

  Matjaz Gregoric

* Fix typo in TTFunk::Subset::Unicode#includes?

  Matjaz Gregoric

* Fixe calculation of search_range for font subsets

  Matjaz Gregoric

* Fixed instance variable @offset and @length not initialized

  Katsuya HIDAKA

* Code style fixes

  Katsuya HIDAKA, Matjaz Gregoric, Alexander Mankuta

## [1.5.1]

### Fixed

* loca table corruption during subsetting. The loca table serialization code
  didn't properly detect suitable table format.

* Fixed checksum calculation for empty tables.

## [1.5.0] - 2017-02-13

### Added

* Support for reading TTF fonts from TTC files

### Changed

* Subset font naming is consistent now and depends on content


## [1.4.0] - 2014-09-21

### Added

* sbix table support


## [1.3.0] - 2014-09-10

### Removed

* Post table version 2.5


## [1.2.2] - 2014-08-29

### Fixed

* Ignore unsupported cmap table versions


## [1.2.1] - 2014-08-28

### Fixed

* Added missing Pathname require


## [1.2.0] - 2014-06-23

### Added

* Rubocop checks
* Ability to parse IO objects

### Changed

* Improved preferred family name selection


## [1.1.1] - 2014-02-24

### Changed

* Clarified licensing

### Removed

* comicsans.ttf


## [1.1.0] - 2014-01-21

### Added

* Improved Unicode astral planes support
* Support for cmap table formats 6, 10, 12
* RSpec-based specs

### Fixed

* Subsetting in JRuby


## [1.0.3] - 2011-10-11

### Added

* Authorship information


## 1.0.2 - 2011-08-08

### Fixed

* Ruby 1.9.2 segmentation fault on Enumerable#zip(range)


## 1.0.0 - 2011-04-02 [YANKED]

Initial release as a standalone gem



[Unreleased]: https://github.com/prawnpdf/ttfunk/compare/1.7.0...HEAD
[1.7.0]: https://github.com/prawnpdf/ttfunk/compare/1.6.2.1...1.7.0
[1.6.2.1]: https://github.com/prawnpdf/ttfunk/compare/1.6.2...1.6.2.1
[1.6.2]: https://github.com/prawnpdf/ttfunk/compare/1.6.1...1.6.2
[1.6.1]: https://github.com/prawnpdf/ttfunk/compare/1.6.0...1.6.1
[1.6.0]: https://github.com/prawnpdf/ttfunk/compare/1.5.1...1.6.0
[1.5.1]: https://github.com/prawnpdf/ttfunk/compare/1.5.0...1.5.1
[1.5.0]: https://github.com/prawnpdf/ttfunk/compare/1.4.0...1.5.0
[1.4.0]: https://github.com/prawnpdf/ttfunk/compare/1.3.0...1.4.0
[1.3.0]: https://github.com/prawnpdf/ttfunk/compare/1.2.2...1.3.0
[1.2.2]: https://github.com/prawnpdf/ttfunk/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/prawnpdf/ttfunk/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/prawnpdf/ttfunk/compare/1.1.1...1.2.0
[1.1.1]: https://github.com/prawnpdf/ttfunk/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/prawnpdf/ttfunk/compare/1.0.3...1.1.0
[1.0.3]: https://github.com/prawnpdf/ttfunk/compare/1.0.2...1.0.3
