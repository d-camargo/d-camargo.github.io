# frozen_string_literal: true

source "https://rubygems.org"
gemspec

bundle install
bundle exec jekyll serve --source blog

gem "jekyll", ENV["JEKYLL_VERSION"] if ENV["JEKYLL_VERSION"]
gem "kramdown-parser-gfm" if ENV["JEKYLL_VERSION"] == "~> 3.9"
