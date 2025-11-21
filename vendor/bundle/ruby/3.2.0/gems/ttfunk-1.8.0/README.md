# TTFunk

![Maintained: yes](https://img.shields.io/badge/maintained-yes-brightgreen.svg)
![CI status](https://github.com/prawnpdf/ttfunk/workflows/CI/badge.svg)

TTFunk is a TrueType and OpenType font library written in pure ruby. It supports
both parsing and encoding of fonts. Also provides limited font subsetting.

## Installation

The recommended installation method is via Rubygems.

```shell
gem install ttfunk
```

## Usage

Basic usage:

```ruby
require 'ttfunk'

file = TTFunk::File.open("some/path/myfont.ttf")
puts "name    : #{file.name.font_name.join(', ')}"
puts "ascent  : #{file.ascent}"
puts "descent : #{file.descent}"
```

For more detailed examples, explore the examples directory.

## Licensing

Matz's terms for Ruby, GPLv2, or GPLv3. See LICENSE for details.

##  Authorship

This project is maintained by the same folks who run the Prawn PDF project.

Here's the [full list](https://github.com/prawnpdf/ttfunk/contributors) of
Github users who have at least one patch accepted to TTFunk.

## Community support

TTFunk is maintained as a dependency of Prawn, the ruby PDF generation library.

Any questions or feedback should be sent to the [Prawn
Diccussions](https://github.com/orgs/prawnpdf/discussions) group.
