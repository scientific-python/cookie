# frozen_string_literal: true

source 'https://rubygems.org'

# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!

gem 'jekyll'

# This is the theme
gem 'just-the-docs'

# This is needed for GitHub Flavored Markdown
gem 'kramdown-parser-gfm'

# Used to be in the stdlib
gem 'logger'

# If you have any plugins, put them here!
group :jekyll_plugins do
  gem 'jekyll-feed'
  gem 'jekyll-seo-tag'
end

group :development do
  # Verify good coding practices in Ruby files
  gem 'rubocop', '~>1.52', require: false

  # Check links. Use:
  #   bundle exec jekyll build
  #   bundle exec htmlproofer --assume_extension '.html' ./_site
  gem 'html-proofer'
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem 'tzinfo'
  gem 'tzinfo-data'
end

gem 'wdm', install_if: Gem.win_platform?
