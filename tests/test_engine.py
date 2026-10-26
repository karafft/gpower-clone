import json
import math
import subprocess
import sys
import unittest
from gpower_clone import analyze, AnalysisError, serialize

def call(mode, **kw):
    return analyze(dict(test="t2-indep", mode=mode, tails=1, **kw))

class EngineTests(unittest.TestCase):
    def close(self, actual, expected):
        for k,v in expected.items():
            if type(v) is int: self.assertIs(type(actual[k]), int); self.assertEqual(actual[k], v)
            else: self.assertTrue(math.isclose(actual[k], v, rel_tol=1e-6, abs_tol=1e-6), (k, actual[k], v))
    def test_public_vectors(self):
        common = dict(ncp=3.3166248, df=174)
        self.close(call("a-priori", d=.5, alpha=.05, power=.95, ratio=1), dict(common, critical_t=1.6536580, n1=88,n2=88,n_total=176,actual_power=.9514254))
        self.close(call("post-hoc", d=.5, alpha=.05,n1=88,n2=88), dict(common,critical_t=1.6536580,power=.9514254))
        self.close(call("compromise",d=.5,beta_alpha_ratio=1,n1=88,n2=88),dict(common,critical_t=1.6606859,alpha=.0492887,beta=.0492887,power=.9507113))
        self.close(call("criterion",d=.5,power=.95,n1=88,n2=88),dict(common,critical_t=1.6676050,alpha=.0485965))
        self.close(call("sensitivity",alpha=.05,power=.95,n1=88,n2=88),dict(ncp=3.3025887,critical_t=1.6536580,df=174,d=.4978840))
    @staticmethod
    def continuous_reference(p):
        # Independently bisect the fractional-allocation equation, not rounded powers.
        from scipy.stats import t,nct
        def power(total):
            n1=total/(1+p["ratio"]); n2=total-n1
            delta=p["d"]*math.sqrt(n1*n2/total);df=total-2
            c=t.isf(p["alpha"]/p["tails"],df)
            return float(nct.sf(c,df,delta)+(nct.cdf(-c,df,delta) if p["tails"]==2 else 0))
        lo,hi=4.,4.
        if power(lo)>=p["power"]: return lo
        while power(hi)<p["power"]: hi*=2
        for _ in range(80):
            mid=(lo+hi)/2
            if power(mid)>=p["power"]:hi=mid
            else:lo=mid
        return (lo+hi)/2
    def test_continuous_solve_then_round_pipeline(self):
        from gpower_clone.engine import core
        for tails in (1,2):
            for ratio in (.3,1,1.7):
                p=dict(test="t2-indep",mode="a-priori",tails=tails,d=.7,alpha=.05,power=.8,ratio=ratio)
                r=analyze(p)
                root=self.continuous_reference(p)
                self.assertAlmostEqual(core._continuous_total(p),root,places=7)
                n1,n2=core._allocate_total(core._round_even_total(root),ratio)
                self.assertEqual((r["n1"],r["n2"]),(n1,n2))
                post=analyze(dict(test="t2-indep",mode="post-hoc",tails=tails,d=p["d"],alpha=p["alpha"],n1=n1,n2=n2))
                self.assertEqual(r["actual_power"],post["power"])
    def test_observed_pre_round_and_once_only_correction(self):
        from gpower_clone.engine.core import _round_even_total,_allocate_total
        x=6+8e-11
        self.assertEqual(2*math.ceil(x/2),8)
        self.assertEqual(_round_even_total(x),6)
        self.assertEqual(_round_even_total(6+1.2e-10),8)
        self.assertEqual(_allocate_total(1_000_000_000,1+5e-9),(500_000_000,500_000_001))
        # One increment can leave unequal groups and an odd final total.
        self.assertEqual(sum(_allocate_total(1_000_000_000,1+5e-9))%2,1)
    def test_no_post_round_power_optimization(self):
        from scipy.stats import t,nct
        total=20.;ratio=1.7;d=.5;alpha=.05;df=total-2
        n1=total/(1+ratio);n2=total-n1;delta=d*math.sqrt(n1*n2/total)
        target=float(nct.sf(t.isf(alpha,df),df,delta))
        result=analyze(dict(test="t2-indep",mode="a-priori",tails=1,d=d,alpha=alpha,power=target,ratio=ratio))
        self.assertEqual((result["n1"],result["n2"],result["n_total"]),(7,13,20))
        self.assertLess(result["actual_power"],target)
    def test_corrected_spec_allocations(self):
        for ratio,n1,n2,total in [(1.5,54,80,134),(1.3,57,73,130),(.7,78,54,132),(2.5,45,111,156),(1.1,61,67,128)]:
            self.close(analyze(dict(test="t2-indep",mode="a-priori",tails=2,d=.5,alpha=.05,power=.8,ratio=ratio)),dict(n1=n1,n2=n2,n_total=total))
        self.close(analyze(dict(test="t2-indep",mode="a-priori",tails=2,d=.35,alpha=.025,power=.88,ratio=1.25)),dict(n1=173,n2=217,n_total=390))
        self.close(analyze(dict(test="t2-indep",mode="a-priori",tails=2,d=.6,alpha=.0001,power=.8,ratio=1)),dict(n1=129,n2=129,n_total=258))
    def test_equality_and_below_alpha(self):
        for tails in (1,2):
            self.close(analyze(dict(test="t2-indep",mode="a-priori",tails=tails,d=.5,alpha=.05,power=.05,ratio=1)),dict(n1=2,n2=2,n_total=4))
        with self.assertRaises(AnalysisError) as ctx: call("a-priori",d=.5,alpha=.05,power=.04,ratio=1)
        self.assertEqual(ctx.exception.code,"INCONSISTENT")
    def test_sensitivity_mathematical_equality(self):
        from scipy.stats import t
        from unittest.mock import patch
        for tails in (1,2):
            r=analyze(dict(test="t2-indep",mode="sensitivity",tails=tails,alpha=.05,power=.05,n1=20,n2=31))
            self.close(r,dict(ncp=0.0,d=0.0,df=49,critical_t=float(t.isf(.05/tails,49))))
        # Exact input equality has its own boundary; nearby inputs still use inverse solving.
        with patch("scipy.optimize.brentq",return_value=1e-10) as root:
            call("sensitivity",alpha=.05,power=math.nextafter(.05,1.0),n1=20,n2=31)
            root.assert_called_once()
    def test_nonfinite_sf_fallback(self):
        from unittest.mock import patch
        from gpower_clone.engine import core
        expected=call("post-hoc",d=.6,alpha=.0001,n1=129,n2=129)["power"]
        with patch.object(core.nct,"sf",return_value=float("nan")):
            actual=call("post-hoc",d=.6,alpha=.0001,n1=129,n2=129)["power"]
        self.assertAlmostEqual(actual,expected,places=12)
        # No CDF complement is consulted if SF already supplies valid probability.
        with patch.object(core.nct,"cdf",side_effect=AssertionError("unnecessary cdf")):
            self.assertAlmostEqual(call("post-hoc",d=.6,alpha=.0001,n1=129,n2=129)["power"],expected)
        with patch.object(core.nct,"sf",return_value=float("nan")),patch.object(core.nct,"cdf",return_value=float("nan")):
            with self.assertRaises(AnalysisError) as ctx: call("post-hoc",d=.5,alpha=.05,n1=20,n2=20)
            self.assertEqual(ctx.exception.code,"NO_SOLUTION")
        expected_two=analyze(dict(test="t2-indep",mode="post-hoc",tails=2,d=.6,alpha=.0001,n1=129,n2=129))["power"]
        with patch.object(core.nct,"cdf",return_value=float("nan")):
            recovered=analyze(dict(test="t2-indep",mode="post-hoc",tails=2,d=.6,alpha=.0001,n1=129,n2=129))["power"]
        self.assertAlmostEqual(recovered,expected_two,places=12)
    def test_inverse_and_compromise(self):
        for tails in (1,2):
            base=dict(test="t2-indep",tails=tails,n1=30,n2=43)
            s=analyze(dict(base,mode="sensitivity",alpha=.03,power=.85))
            self.assertAlmostEqual(analyze(dict(base,mode="post-hoc",alpha=.03,d=s["d"]))["power"],.85,places=10)
            c=analyze(dict(base,mode="criterion",d=.6,power=.8))
            self.assertAlmostEqual(analyze(dict(base,mode="post-hoc",d=.6,alpha=c["alpha"]))["power"],.8,places=10)
            q=analyze(dict(base,mode="compromise",d=.6,beta_alpha_ratio=2.5))
            self.assertAlmostEqual(q["beta"]/q["alpha"],2.5,places=9)
    def test_central_t_independent_identity(self):
        # Student t(df=2) has closed-form positive-tail probability.
        from scipy.stats import t
        for x in (.1,1,3):
            self.assertAlmostEqual(t.sf(x,2),.5-x/(2*math.sqrt(x*x+2)),places=13)
    def test_validation(self):
        base=dict(test="t2-indep",mode="post-hoc",tails=1,d=.5,alpha=.05,n1=30,n2=30)
        for field,value,code in [("alpha",0,"OUT_OF_RANGE"),("d","nan","INVALID_VALUE"),("d","0,5","INVALID_VALUE"),("n1",2.0,"INVALID_VALUE"),("n2",1,"OUT_OF_RANGE"),("tails",3,"OUT_OF_RANGE"),("d",True,"INVALID_VALUE"),("test","other","UNSUPPORTED"),("mode","other","UNSUPPORTED"),("extra",1,"UNKNOWN_PARAM")]:
            with self.subTest(field=field,value=value):
                with self.assertRaises(AnalysisError) as ctx: analyze(dict(base,**{field:value}))
                self.assertEqual(ctx.exception.code,code)
        del base["d"]
        with self.assertRaises(AnalysisError) as ctx: analyze(base)
        self.assertEqual(ctx.exception.code,"MISSING_PARAM")
        with self.assertRaises(AnalysisError) as ctx: call("sensitivity",alpha=.1,power=.05,n1=10,n2=10)
        self.assertEqual(ctx.exception.code,"INCONSISTENT")
        with self.assertRaises(AnalysisError) as ctx: call("a-priori",d=1e-5,alpha=.05,power=.8,ratio=.01)
        self.assertEqual(ctx.exception.code,"NO_SOLUTION")
    def test_serializer(self):
        self.assertEqual(json.loads(serialize({"x":1.2345678901234567}))["x"],1.2345678901234567)

    def test_a_priori_effect_domain_boundary(self):
        from gpower_clone.engine.core import _validate
        base=dict(test="t2-indep",mode="a-priori",tails=2,d=1e-5,alpha=.05,power=.8,ratio=1)
        below=math.nextafter(1e-5,0.0)
        with self.assertRaises(AnalysisError) as ctx: _validate(dict(base,d=below))
        self.assertEqual((ctx.exception.code,ctx.exception.field),("OUT_OF_RANGE","d"))
        for d in (1e-5,math.nextafter(1e-5,math.inf)):
            self.assertEqual(_validate(dict(base,d=d))["d"],d)
        # The a-priori threshold is not generalized to post-hoc or inverse modes.
        self.assertEqual(_validate(dict(test="t2-indep",mode="post-hoc",tails=2,d=below,alpha=.05,n1=20,n2=20))["d"],below)
        with self.assertRaises(AnalysisError) as ctx: analyze(base)
        self.assertEqual(ctx.exception.code,"NO_SOLUTION")

    def test_large_feasible_continuous_pipeline(self):
        from gpower_clone.engine.core import _round_even_total,_allocate_total
        p=dict(test="t2-indep",mode="a-priori",tails=2,d=.0005,alpha=.05,power=.8,ratio=1)
        result=analyze(p)
        self.assertGreater(result["n_total"],20_000_000)
        for key in ("n1","n2","n_total","df"): self.assertIs(type(result[key]),int)
        self.assertTrue(all(math.isfinite(v) for v in result.values()))
        reference=self.continuous_reference(p)
        self.assertEqual((result["n1"],result["n2"]),_allocate_total(_round_even_total(reference),1))

    def test_observed_inclusive_ranges_and_neighbors(self):
        from gpower_clone.engine.core import _validate
        for field,low,high,base in [
            ("alpha",1e-7,.9999999,dict(test="t2-indep",mode="post-hoc",tails=2,d=.5,alpha=.05,n1=20,n2=30)),
            ("power",1e-7,.9999999,dict(test="t2-indep",mode="criterion",tails=2,d=.5,power=.8,n1=20,n2=30)),
            ("ratio",.01,100.,dict(test="t2-indep",mode="a-priori",tails=2,d=.5,alpha=.05,power=.8,ratio=1))]:
            for value in (low,high,math.nextafter(low,high),math.nextafter(high,low)):
                self.assertEqual(_validate(dict(base,**{field:value}))[field],value)
            for value in (math.nextafter(low,-math.inf),math.nextafter(high,math.inf)):
                with self.subTest(field=field,value=value):
                    with self.assertRaises(AnalysisError) as ctx: _validate(dict(base,**{field:value}))
                    self.assertEqual((ctx.exception.code,ctx.exception.field),("OUT_OF_RANGE",field))
        with self.assertRaises(AnalysisError) as ctx:
            _validate(dict(test="t2-indep",mode="post-hoc",tails=2,d=.5,alpha=.05,n1=20,n2=30,ratio=1))
        self.assertEqual(ctx.exception.code,"UNKNOWN_PARAM")

if __name__ == "__main__": unittest.main()
