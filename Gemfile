# frozen_string_literal: true

source "https://rubygems.org"
gemspec

gem "jekyll", "~> 4.2"

group :jekyll_plugins do
  gem "jekyll-timeago", "~> 0.13.1"
end

gem "jekyll", ENV["JEKYLL_VERSION"] if ENV["JEKYLL_VERSION"]
gem "kramdown-parser-gfm" if ENV["JEKYLL_VERSION"] == "~> 3.9"
