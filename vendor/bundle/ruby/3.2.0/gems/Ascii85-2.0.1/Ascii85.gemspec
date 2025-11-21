# frozen_string_literal: true

require_relative 'lib/Ascii85/version'

Gem::Specification.new do |s|
  s.name        = 'Ascii85'
  s.version     = Ascii85::VERSION
  s.platform    = Gem::Platform::RUBY
  s.author      = 'Johannes Holzfuß'
  s.email       = 'johannes@holzfuss.name'
  s.license     = 'MIT'
  s.homepage    = 'https://github.com/DataWraith/ascii85gem/'
  s.summary     = 'Ascii85 encoder/decoder'
  s.description = "Ascii85 provides methods to encode/decode Adobe's binary-to-text encoding of the same name."

  s.required_ruby_version = '>= 2.7.0'

  s.add_development_dependency 'minitest', '~> 5', '>= 5.12.0'
  s.add_development_dependency 'rake', '~> 13'

  s.files            = `git ls-files`.split("\n") - ['.gitignore', '.github/workflows/ruby.yml']
  s.test_files       = `git ls-files -- spec/*`.split("\n")
  s.executables      = `git ls-files -- bin/*`.split("\n").map { |f| File.basename(f) }
  s.require_paths    = ['lib']
  s.extra_rdoc_files = ['README.md', 'LICENSE']
end
