# Synthetic Ruby group fixtures

These small fixtures demonstrate only supplied-file declaration membership.
They do not describe an application, installation, runtime, deployment, or
publication history. T001 uses Gemfiles only; lock association is a later task.

| Fixture | Expected recognition / selected population |
|---|---|
| `memberships.Gemfile` | Accepted. `default` selects rack; `test` or `development` selects rake and debug; `Test` selects debug; `bench` selects none. `default` plus `test` selects rack, rake and debug once each. All five names are established, preserving case. Optionality does not change membership. |
| `duplicate.Gemfile` | Reject all scope with `duplicate_gemfile_declaration`, line 5. No partial rack population. |
| `unsupported.Gemfile` | Reject all scope with `unsupported_gemfile_syntax`, line 5, including when `unselected` was not requested. No partial rack population. |
