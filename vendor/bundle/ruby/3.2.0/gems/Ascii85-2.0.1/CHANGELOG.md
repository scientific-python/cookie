# Ascii85 Changelog

## [2.0.1] - 2024-09-15

### Fixed

- Decoding binary data could lead to Encoding errors (Issue #8)

## [2.0.0] - 2024-08-20

### BREAKING CHANGES

- The minimum required Ruby version has been raised to 2.7.0.

### Added

- `Ascii85.decode_raw` method that doesn't expect the input to be wrapped in `<~` and `~>` delimiters.
- `Ascii85.extract` method to extract encoded text from between `<~` and `~>` for feeding to `#decode_raw`.
- Option to pass an IO-object as input to `#encode` and `#decode_raw` instead of a String.
- Option to pass an IO-object to `#encode` and `#decode_raw` for output. Output is written to the object instead of being returned as a String.
- Streaming capability for `#encode` and `#decode_raw` when both input and output are IO objects, using constant memory.

## [1.1.1] - 2024-05-09

### Fixed

- Make `bin/ascii85` Ruby 3.2-compatible (thanks @tylerwillingham)
- Slightly improved error handling of `bin/ascii85`

## [1.1.0] - 2020-11-11

### Added

- Make use of frozen_string_literal (thanks @aliismayilov)

### Changed

- Updated tests to use newer minitest syntax

## [1.0.3] - 2018-01-25

### Changed

- Updated the gem's metadata

## [1.0.2] - 2012-09-16

### Changed

- Changed test runner from RSpec to MiniSpec
- Added support for rubygems-test
- Minor changes to make packaging easier

## [1.0.1] - 2011-05-05

### Changed

- Removed `hoe` dependency in favor of `bundler`
- Minor corrections in the documentation

## [1.0.0] - 2009-12-25

### Added

- Ruby 1.9 compatibility
- Command-line en- and decoder

## [0.9.0] - 2009-02-17

- Initial release
