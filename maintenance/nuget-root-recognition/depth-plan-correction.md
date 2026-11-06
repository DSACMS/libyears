# Depth-boundary architecture and task correction

Governing specification amendment: [depth-spec-correction.md](depth-spec-correction.md),
SHA256 `eb9cc925d715c9da18a32831d1765a5a888bf94294eb9e43f993adad18f97048`,
independently APPROVED in reviews.md. Original spec/plan/task bytes stay frozen;
this supplement supersedes only their depth-overflow mechanism and witness.

Replace `raise _IncompleteRecognition` at the `depth == MAX_DEPTH` directory
branch with `continue`. It must occur before opening the child directory.
Do not alter MAX_DEPTH or any other limit, capability, error, identity, metadata,
format_json/scan/model/adapter behavior. Add human disclosure that count/list
covers only root through depth four, excluding hidden/generated/dependency
directories. Revise README/SPEC current guidance to match; historic Feature 006
artifacts and original reviewed maintenance candidates stay unchanged.

One bounded corrective task **D1**, predecessor approved amendment and this
architecture/task review, repairs C1/C2's depth rule before C3 resumes:

- Update discovery depth behavior with its behavioral test: depth-four candidate
  included, a depth-five candidate and directory pruned without an open or scan,
  nested excluded directories remain excluded. All count/error/cleanup tests pass.
- Update human disclosure and corresponding injected-evidence assertion; preserve
  all numeric, JSON, explicit-selection and no-implicit-choice witnesses.
- Run focused discovery/recognition/shared CLI-output tests, full offline suite
  and full capability-disabled simulation. Inspect diff/check and create one
  corrective local commit. This replaces no earlier task commit or history.
- Resume C3: repeat the exact authorized OASim command once and compare against
  the original before-manifest plus renewed after-manifest. Preserve initial
  smoke/diagnosis and all errors as historical evidence. Record R1–R6 and real
  worker/GitLeaks checks; freeze the corrected implementation and operational
  evidence for fresh independent K1 convergence. No target package execution,
  input writing, implicit choice or measurement is introduced.

This plan/task correction is itself frozen before fresh non-author review.
Only after approval does D1 execute. Any bounded review defect follows canonical
correction/freeze/fresh verification. New human authority hard stops are unchanged.
