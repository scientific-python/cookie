# -*- encoding: utf-8 -*-
# stub: Ascii85 2.0.1 ruby lib

Gem::Specification.new do |s|
  s.name = "Ascii85".freeze
  s.version = "2.0.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Johannes Holzfu\u00DF".freeze]
  s.date = "2024-09-15"
  s.description = "Ascii85 provides methods to encode/decode Adobe's binary-to-text encoding of the same name.".freeze
  s.email = "johannes@holzfuss.name".freeze
  s.executables = ["ascii85".freeze]
  s.extra_rdoc_files = ["README.md".freeze, "LICENSE".freeze]
  s.files = ["LICENSE".freeze, "README.md".freeze, "bin/ascii85".freeze]
  s.homepage = "https://github.com/DataWraith/ascii85gem/".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.7.0".freeze)
  s.rubygems_version = "3.4.20".freeze
  s.summary = "Ascii85 encoder/decoder".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_development_dependency(%q<minitest>.freeze, ["~> 5", ">= 5.12.0"])
  s.add_development_dependency(%q<rake>.freeze, ["~> 13"])
end
