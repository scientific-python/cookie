# -*- encoding: utf-8 -*-
# stub: afm 1.0.0 ruby lib

Gem::Specification.new do |s|
  s.name = "afm".freeze
  s.version = "1.0.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Jan Krutisch".freeze]
  s.date = "2025-06-12"
  s.description = "a simple library to read afm files and use the data conveniently".freeze
  s.email = "jan@krutisch.de".freeze
  s.extra_rdoc_files = ["LICENSE".freeze, "README.md".freeze]
  s.files = ["LICENSE".freeze, "README.md".freeze]
  s.homepage = "http://github.com/halfbyte/afm".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 3.2.0".freeze)
  s.rubygems_version = "3.4.20".freeze
  s.summary = "reading Adobe Font Metrics (afm) files".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_development_dependency(%q<rake>.freeze, ["~> 13.3"])
  s.add_development_dependency(%q<rdoc>.freeze, ["~> 6.14"])
  s.add_development_dependency(%q<minitest>.freeze, ["~> 5.25"])
end
