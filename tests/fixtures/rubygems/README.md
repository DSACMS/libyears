# RubyGems fixtures

The JSON files are synthetic, offline examples, not captured package history.
They follow the immutable RubyGems.org source chain pinned by Feature 004:
`9d5892f97d320b8d5ca8446f7119743afeb97183`.

All paths below are relative to
https://github.com/rubygems/rubygems.org/tree/9d5892f97d320b8d5ca8446f7119743afeb97183/.

- `app/controllers/api/v1/rubygems_controller.rb`: public show requires hosted,
  indexed versions; `app/models/rubygem.rb` payload establishes name identity.
- `app/controllers/api/v1/versions_controller.rb`: show serializes the complete
  public_versions relation without pagination, and returns 404 when empty.
- `app/models/rubygem.rb`: public_versions uses by_position.published.
- `app/models/version.rb`: published/indexed filtering establishes availability;
  payload/as_json exposes number, platform, ruby_abi, prerelease, created_at and
  built_at. ABI identity permits null or major.minor and participates in uniqueness.

Population records omit names; identity.json therefore establishes identity
independently. Package-selected version and gem_uri are deliberately ignored.
Creation time alone supplies publication evidence; built_at is never a fallback.
Ordinary population records are currently indexed/published; absence does not
establish yanking or historical nonexistence. Synthetic normalized yanked records
in helper tests exercise future observable evidence without claiming this wire
endpoint exposes yank history. Explicit wire yank assertions contradict membership.
