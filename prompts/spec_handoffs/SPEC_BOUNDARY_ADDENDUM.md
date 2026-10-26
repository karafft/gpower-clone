# Clean implementation boundary addendum

New analyzed rule, supply only behavior to implementation session; do not inspect raw executable or evidence.

- A-priori d must be at least 1e-5. Reject positive d<1e-5 with OUT_OF_RANGE field d. The endpoint 1e-5 passes this domain check. General CONTRACT still rejects d<=0 for every mode. Do not impose the a-priori threshold on other modes. Rule source label REA-STATIC-003, analyzed separately by coordinator; not a new empirical oracle fixture.
- Raise the even-total engineering search ceiling from20,000,000 to2,147,483,646 (largest allowed even 32bit total). This upper bracket is consistent with analyzed validation bound; still document candidate search behavior and arithmetic guard. At/below effect threshold, failure to attain target within total ceiling remains NO_SOLUTION rather than an endless search. This does not impose an unobserved maximum on arbitrary post-hoc group inputs.
- Add meaningful boundary tests for d immediately below/at/above1e-5, keeping runtime bounded. Domain validator testing is permitted to distinguish acceptance from search infeasibility.
- Add one large-N but feasible case (e.g. d0.0005 alpha.05 power.8 ratio1 tails2) to ensure the old20m guard no longer wrongly returns NO_SOLUTION. Verify target attainment, previous even-total minimality and integer fields rather than assuming an externally observed N.
- Preserve prior1.1 public/regression/protocol behavior; no vector-specific rules. Version1.1.0rc2 consistently and rebuild/install check. Parent independently reruns the external development suite.
