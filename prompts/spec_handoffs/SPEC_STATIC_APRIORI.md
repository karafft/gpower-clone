# A-priori static-analysis behavior replacement for clean implementation

This standalone behavioral specification supersedes the candidate minimal-even-INTEGER-power search. Parent has now analyzed the real t2-indep call path and arithmetic helpers. Do NOT open raw executable, ledger, oracle data or static-analysis reports; use only these semantic rules. Other modes and rc3 confirmed input bounds remain.

## Continuous solve then round, not integer power optimization

1. Solve continuous total x for target power using fractional allocations n1=x/(1+r), n2=x-n1, df=x-2 and delta=d*sqrt(n1*n2/x). Apply same t/noncentral-t tails math. Do NOT search already-rounded allocations for minimal power.
2. If target is reached at x=4, use continuous lower clamp4 (the post-rounded lower domain). Otherwise bracket exponentially up to maximum total2,147,483,646 then solve root; use brentq with xtol~1e-10 and bounded300 iterations. If root cannot be bracketed within guard, NO_SOLUTION. Exact original solver has its own numerical path; do not claim bit-identical roots.
3. Round continuous total by this semantic helper:
   q=x/2;
   rounded10=floor(q*1e10+0.5)/1e10;
   N=2*ceil(rounded10).
   This 10-decimal pre-round and ceiling are observed arithmetic, not output decimal rounding. Retain full precision for output values.
4. n1=floor(N/(1+r)+0.5) (half-up). n2=ceil(N-n1). Do not impose n2=ceil(n1*r).
5. If abs(r-1)<1e-8 AND abs(n1-n2)>1e-8, increment the smaller group ONCE by1. This is the observed nearly-equal allocation correction, not a loop.
6. Compute reported n_total=n1+n2, df=n_total-2, delta and actual_power from FINAL integer allocation. Do not add more subjects solely because rounding made actual_power slightly below target. That is behavior; do not silently optimize it away.
7. Keep documented engineering refusal for unsupported nonpositive/too-small allocated groups if necessary; no GUI evidence for equality+extreme ratio corner, do not assert source parity there. All already-supplied regression allocations still expected to pass. CONTRACT provided sample inputs n1/n2 remain>=2 strictint.

## Evidence status

The source call chain uses a continuous scalar solver, calls an even-total rounding helper, then half-up first-group and ceil second-group helpers and evaluates power once. This corrects previous candidate search semantics; constants and procedure are supplied here without decompiled code. Implementation can independently choose bracketing/root algorithms consistent with that semantic pipeline.

Version1.1.0rc4. Replace obsolete test claiming minimal even integer POWER with tests of continuous-solve/round pipeline and independent continuous fractional power root consistency. Keep all public values, unequal allocation regression examples, range boundaries and inverse tests. Add tiny pre-round helper tests that distinguish unroundedceil from observed10-decimal pre-round. A large-N case should validate finite fields and correct pipeline; previous-allocated-power minimality is no longer valid generally. No vector hardcoding or raw evidence.

Final software tests (CLI, real MCP parity, mocked provider, evaluator no-key, installed commands), changelog and machine summary; parent does external dataset and final packaging. No further feature expansion, no repository changes.
