# -*- encoding: utf-8 -*-
# stub: html-proofer 5.0.10 ruby lib

Gem::Specification.new do |s|
  s.name = "html-proofer".freeze
  s.version = "5.0.10"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "funding_uri" => "https://github.com/sponsors/gjtorikian/", "rubygems_mfa_required" => "true" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Garen Torikian".freeze]
  s.bindir = "exe".freeze
  s.date = "2025-02-21"
  s.description = "Test your rendered HTML files to make sure they're accurate.".freeze
  s.email = ["gjtorikian@gmail.com".freeze]
  s.executables = ["htmlproofer".freeze]
  s.files = ["exe/htmlproofer".freeze]
  s.homepage = "https://github.com/gjtorikian/html-proofer".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new([">= 3.1".freeze, "< 4.0".freeze])
  s.rubygems_version = "3.4.20".freeze
  s.summary = "A set of tests to validate your HTML output. These tests check if your image references are legitimate, if they have alt tags, if your internal links are working, and so on. It's intended to be an all-in-one checker for your documentation output.".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_runtime_dependency(%q<addressable>.freeze, ["~> 2.3"])
  s.add_runtime_dependency(%q<async>.freeze, ["~> 2.1"])
  s.add_runtime_dependency(%q<nokogiri>.freeze, ["~> 1.13"])
  s.add_runtime_dependency(%q<pdf-reader>.freeze, ["~> 2.11"])
  s.add_runtime_dependency(%q<rainbow>.freeze, ["~> 3.0"])
  s.add_runtime_dependency(%q<typhoeus>.freeze, ["~> 1.3"])
  s.add_runtime_dependency(%q<yell>.freeze, ["~> 2.0"])
  s.add_runtime_dependency(%q<zeitwerk>.freeze, ["~> 2.5"])
  s.add_development_dependency(%q<rspec>.freeze, ["~> 3.1"])
  s.add_development_dependency(%q<timecop>.freeze, ["~> 0.8"])
  s.add_development_dependency(%q<vcr>.freeze, ["~> 2.9"])
end
