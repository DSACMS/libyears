# Synthetic declarations: default, overlapping explicit groups, and empty bench.
source "https://rubygems.org"
gem "rack"
group :test, :development, optional: true do
  gem "rake", ">= 1", "< 3"
  gem "debug", groups: [:Test, :test], require: false
end
group :bench do
end
