# t2-indep corrected implementation specification 1.1 candidate

This is a standalone behavior supplement to the previously supplied SPEC and CONTRACT1.0.0. It is a behavioral inference fitted to development observations, not binary REA proof. Do not access raw oracle evidence. Keep other modes/interfaces as previously specified.

## A-priori allocation replacement

Replace n2=ceil(n1*ratio) and minimal n1 search. Candidate behavior:

- Search total N=2*k with integer k>=2 (even total starting at4).
- Allocate n1=floor(N/(1+ratio)+0.5), n2=N-n1. Use arithmetic half-up, not language bankers rounding.
- Both group sizes must be at least2. Skip smaller candidates.
- df=N-2. ncp=d*sqrt(n1*n2/N).
- Compute critical_t using central t inverse survival alpha/tails.
- Compute power using specified noncentral t tails. Return the smallest valid even total meeting target power, and its allocation.
- Exponential bracket and binary search over k are permitted because both allocated group sizes are nondecreasing with increasing k. Output and N bounds must be documented as engineering bounds unless independently proven.
- Positive d, ratio; finite inputs and existing CONTRACT type/range rules persist. Keep checks for unknown/irrelevant/missing fields.

## Equality

For a-priori reject power<alpha; allow power==alpha and perform the normal minimum N search. Do not generalize this empirical rule to sensitivity without evidence: preserve/document current sensitivity handling as provisional.

## Numerical stability

The specified formula is right_tail=1-nct.cdf(c,df,delta); for improved precision nct.sf is allowed. If sf is nonfinite, fall back to 1-cdf; if cdf complement is nonfinite and sf finite use sf. Add left-tail nct.cdf(-c,..) for tails2. Reject only if no finite valid probability is available. Finite results may be clamped to [0,1] only for tiny floating point excursion, not to hide an invalid result. Record numerical backend caveat. Inverse modes use same probability helper.

## Contract versus GUI

Do not accept negative d or fractional n1/n2: CONTRACT explicitly forbids these regardless of GUI behavior. Do not change advertised test family or required inputs. No vector-specific hardcoding.

## Specification status and regression acceptance

Allocation is a general candidate consistent with 38 development N cases; it needs fresh external validation and REA. Half-way tie behavior specifically remains unobserved. Tests must include representative expected allocations from SPEC rather than source oracle inspection: ratio1.5 tails2 d.5 alpha.05 power.8 ->54/80 total134; ratio1.3 same ->57/73 total130; ratio.7 ->78/54 total132; ratio2.5 ->45/111 total156; ratio1.1 ->61/67 total128; ratio1.25 tails2 d.35 alpha.025 power.88 ->173/217 total390. Equality tails1 and tails2 d.5 alpha=power=.05 ratio1 ->2/2 total4. Small alpha tails2 d.6 alpha.0001 power.8 ratio1 ->129/129 total258. Preserve the original five public vectors and inverse tests.

Update the previous minimal-allocation test to enforce minimal valid EVEN TOTAL and this allocation, not the obsolete ceil-ratio rule. Add numerical fallback regression. Preserve pure analyze mapping API, canonical JSON serialization, CLI/MCP equivalence, genuine MCP protocol and live-agent limitations.

Only edit software and its implementation docs. Parent coordinator handles oracle reports and spec provenance. No GitHub writes or publication. Version candidate1.1 consistently, original CONTRACT unchanged.
