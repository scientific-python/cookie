# -*- encoding: utf-8 -*-
# stub: ttfunk 1.8.0 ruby lib

Gem::Specification.new do |s|
  s.name = "ttfunk".freeze
  s.version = "1.8.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "bug_tracker_uri" => "https://github.com/prawnpdf/ttfunk/issues", "changelog_uri" => "https://github.com/prawnpdf/ttfunk/blob/1.8.0/CHANGELOG.md", "documentation_uri" => "https://prwnpdf.org/docs/ttfunk/1.8.0/", "homepage_uri" => "http://prawnpdf.org/", "rubygems_mfa_required" => "true", "source_code_uri" => "https://github.com/prawnpdf/ttfunk" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Alexander Mankuta".freeze, "Gregory Brown".freeze, "Brad Ediger".freeze, "Daniel Nelson".freeze, "Jonathan Greenberg".freeze, "James Healy".freeze, "Cameron Dutro".freeze]
  s.cert_chain = ["-----BEGIN CERTIFICATE-----\nMIIDMjCCAhqgAwIBAgIBAzANBgkqhkiG9w0BAQsFADA/MQ0wCwYDVQQDDARhbGV4\nMRkwFwYKCZImiZPyLGQBGRYJcG9pbnRsZXNzMRMwEQYKCZImiZPyLGQBGRYDb25l\nMB4XDTI0MDMwNDIwMTIyOFoXDTI1MDMwNDIwMTIyOFowPzENMAsGA1UEAwwEYWxl\neDEZMBcGCgmSJomT8ixkARkWCXBvaW50bGVzczETMBEGCgmSJomT8ixkARkWA29u\nZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAM85Us8YQr55o/rMl+J+\nula89ODiqjdc0kk+ibzRLCpfaFUJWxEMrhFiApRCopFDMeGXHXjBkfBYsRMFVs0M\nZfe6rIKdNZQlQqHfJ2JlKFek0ehX81buGERi82wNwECNhOZu9c6G5gKjRPP/Q3Y6\nK6f/TAggK0+/K1j1NjT+WSVaMBuyomM067ejwhiQkEA3+tT3oT/paEXCOfEtxOdX\n1F8VFd2MbmMK6CGgHbFLApfyDBtDx+ydplGZ3IMZg2nPqwYXTPJx+IuRO21ssDad\ngBMIAvL3wIeezJk2xONvhYg0K5jbIQOPB6zD1/9E6Q0LrwSBDkz5oyOn4PRZxgZ/\nOiMCAwEAAaM5MDcwCQYDVR0TBAIwADALBgNVHQ8EBAMCBLAwHQYDVR0OBBYEFE+A\njBJVt6ie5r83L/znvqjF1RuuMA0GCSqGSIb3DQEBCwUAA4IBAQAam5ZgizC0Pknb\nnm7O8fY6+0rdvIP9Zhzbigvfjy664xyZYJ2hJLnvN64wKewcYeYIrC/OEOVbkjWl\nYUDqUfy59JAYvJNQJDi2ZbJPji17WlQaz/x/0QlwWnsYIjOBw0Jyi5Hv41pkMAcO\n+YgdSby0qLIu8sNoTP4YXxRyBuHNBgAUexf3x+dvMyHuM+Q/lKiKmJLwzUlcYr0F\nluk6Jow2lBzuzfjss07L5THk162mtlWVIdtbLsAvcxwTwVZ7W0bKQkyJnTj8gnye\n+ucJ3nnxbYV+GcYHgWdTMu39wjP8z+w+PYLBxpaVjThblqhDQpmIjT4zJvAQALi9\nauxR4ast\n-----END CERTIFICATE-----\n".freeze]
  s.date = "2024-03-04"
  s.description = "Font Metrics Parser for the Prawn PDF generator".freeze
  s.email = ["alex@pointless.one".freeze, "gregory.t.brown@gmail.com".freeze, "brad@bradediger.com".freeze, "dnelson@bluejade.com".freeze, "greenberg@entryway.net".freeze, "jimmy@deefa.com".freeze, "camertron@gmail.com".freeze]
  s.homepage = "http://prawnpdf.org/".freeze
  s.licenses = ["Nonstandard".freeze, "GPL-2.0-only".freeze, "GPL-3.0-only".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.7".freeze)
  s.rubygems_version = "3.4.20".freeze
  s.summary = "TrueType Font Metrics Parser".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_runtime_dependency(%q<bigdecimal>.freeze, ["~> 3.1"])
  s.add_development_dependency(%q<prawn-dev>.freeze, ["~> 0.4.0"])
end
