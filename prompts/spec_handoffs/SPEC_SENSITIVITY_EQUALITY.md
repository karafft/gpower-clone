# Sensitivity equality clarification from original mathematical specification

Original SPEC defines sensitivity as solving nonnegative delta and CONTRACT explicitly says sensitivity reports d>=0. Therefore target power==alpha is the central distribution boundary delta=0,d=0, not an infeasible negative effect. This is a mathematical SPEC clarification, not a newly observed GUI vector.

Sensitivity: reject power<alpha with INCONSISTENT. For exact equality return ncp0.0,d0.0 with the normal critical_t and integer df, without running an ill-conditioned numerical root at zero. Do not round near-equality inputs into equality. Preserve all other inputs/ranges and no defaults.

Test both tails with exact equality and ordinary positive-power inverse cases. Mark this clarification as mathematical, externally unvalidated at the endpoint. Keep rc2 (not yet released) and update final test count/report. No raw evidence access.
