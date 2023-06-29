# frozen_string_literal: true

source "https://rubygems.org"

# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!
gem 'jekyll', '~> 4.3'

# This is the theme
gem "just-the-docs", "~> 0.5.3"

# This is needed for GitHub Flavored Markdown
gem 'kramdown-parser-gfm'

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem 'jekyll-feed'
  gem 'jekyll-seo-tag'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: %i[mingw mswin x64_mingw jruby]

# Performance-booster for watching directories on Windows
gem 'wdm', '~> 0.1.0' if Gem.win_platform?
