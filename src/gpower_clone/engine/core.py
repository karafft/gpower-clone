"""Pure API: no printing, network, random state, or G*Power binaries."""
import json
import math
import re
import platform
from collections.abc import Mapping
from importlib.metadata import version

VERSION = {"contract_version": "1.0.0", "name": "gpower-clone", "engine": f"Python {platform.python_version()} / SciPy {version('scipy')} / SPEC engine 1.1.0rc4"}
FIELDS = {
    "a-priori": {"tails", "d", "alpha", "power", "ratio"},
    "post-hoc": {"tails", "d", "alpha", "n1", "n2"},
    "compromise": {"tails", "d", "beta_alpha_ratio", "n1", "n2"},
    "criterion": {"tails", "d", "power", "n1", "n2"},
    "sensitivity": {"tails", "alpha", "power", "n1", "n2"},
}
# Engineering guards, not observed G*Power limits.
MAX_TOTAL = 2_147_483_646
MAX_DELTA = 1_000_000.0

class AnalysisError(ValueError):
    def __init__(self, code, field, message):
        self.code, self.field = code, field
        super().__init__(message)
    def as_dict(self):
        return {"error": str(self), "code": self.code, "field": self.field}

def fail(code, field, message):
    raise AnalysisError(code, field, message)

def serialize(value):
    """Canonical single-line JSON; preserve Python double precision."""
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))

def _validate(data):
    if not isinstance(data, Mapping):
        fail("INVALID_VALUE", None, "Input must be a mapping")
    for key in ("test", "mode"):
        if key not in data: fail("MISSING_PARAM", key, "Required parameter missing")
    if data["test"] != "t2-indep": fail("UNSUPPORTED", "test", "Unsupported test")
    mode = data["mode"]
    if not isinstance(mode, str) or mode not in FIELDS: fail("UNSUPPORTED", "mode", "Unsupported mode")
    required = FIELDS[mode]
    for key in data:
        if key not in required | {"test", "mode"}: fail("UNKNOWN_PARAM", str(key), "Unknown or irrelevant parameter")
    out = {"mode": mode}
    for key in sorted(required):
        if key not in data: fail("MISSING_PARAM", key, "Required parameter missing")
        raw = data[key]
        if isinstance(raw, bool) or not isinstance(raw, (str, int, float)):
            fail("INVALID_VALUE", key, "Expected numeric value")
        if key in {"tails", "n1", "n2"}:
            if isinstance(raw, float) or (isinstance(raw, str) and not re.fullmatch(r"[+-]?\d+", raw)):
                fail("INVALID_VALUE", key, "Expected integer")
            value = int(raw)
        else:
            if isinstance(raw, str) and not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", raw):
                fail("INVALID_VALUE", key, "Expected decimal-dot number")
            try: value = float(raw)
            except (ValueError, OverflowError): fail("INVALID_VALUE", key, "Expected decimal-dot number")
            if not math.isfinite(value): fail("INVALID_VALUE", key, "Expected finite number")
        if key == "tails" and value not in (1, 2): fail("OUT_OF_RANGE", key, "tails must be 1 or 2")
        if key in {"n1", "n2"} and value < 2: fail("OUT_OF_RANGE", key, "Sample size must be at least 2")
        if key in {"alpha", "power"} and not 0 < value < 1: fail("OUT_OF_RANGE", key, "Expected value strictly between 0 and 1")
        if key in {"alpha", "power"} and not 1e-7 <= value <= .9999999:
            fail("OUT_OF_RANGE", key, "Expected value in inclusive range [1e-7, 0.9999999]")
        if key == "ratio" and not .01 <= value <= 100.0:
            fail("OUT_OF_RANGE", key, "Expected ratio in inclusive range [0.01, 100]")
        if key in {"d", "ratio", "beta_alpha_ratio"} and value <= 0: fail("OUT_OF_RANGE", key, "Expected positive value")
        out[key] = value
    if mode == "a-priori" and out["d"] < 1e-5:
        fail("OUT_OF_RANGE", "d", "A-priori effect size must be at least 1e-5")
    if mode == "a-priori" and out["power"] < out["alpha"]:
        fail("INCONSISTENT", "power", "Target power must be at least alpha")
    if mode == "sensitivity" and out["power"] < out["alpha"]:
        fail("INCONSISTENT", "power", "Sensitivity target power must be at least alpha")
    return out

def _power(c, df, delta, tails):
    def valid(value):
        return math.isfinite(value) and -1e-12 <= value <= 1+1e-12
    right = float(nct.sf(c, df, delta))
    if not valid(right):
        right = 1-float(nct.cdf(c, df, delta))
    if not valid(right): fail("NO_SOLUTION", None, "No finite valid right-tail probability")
    left = float(nct.cdf(-c, df, delta)) if tails == 2 else 0.0
    if not valid(left):
        # Distribution symmetry: F(-c; df, delta) = SF(c; df, -delta).
        left = float(nct.sf(c, df, -delta))
    if not valid(left): fail("NO_SOLUTION", None, "No finite valid left-tail probability")
    result = right + left
    if not valid(result): fail("NO_SOLUTION", None, "No finite valid power probability")
    return min(1.0, max(0.0, result))

def _base(n1, n2, d):
    df = n1 + n2 - 2
    scale = math.sqrt(n1) * math.sqrt(n2 / (n1 + n2))
    return df, d * scale, scale

def _round_even_total(continuous):
    q=continuous/2
    rounded10=math.floor(q*1e10+0.5)/1e10
    return 2*math.ceil(rounded10)


def _allocate_total(total,ratio):
    n1=math.floor(total/(1+ratio)+.5)
    n2=math.ceil(total-n1)
    if abs(ratio-1)<1e-8 and abs(n1-n2)>1e-8:
        if n1<n2: n1+=1
        else: n2+=1
    return n1,n2


def _continuous_total(p):
    def objective(total):
        n1=total/(1+p["ratio"])
        n2=total-n1
        df,delta,_=_base(n1,n2,p["d"])
        if not math.isfinite(delta): fail("NO_SOLUTION","d","Noncentrality exceeds numerical range")
        c=float(t.isf(p["alpha"]/p["tails"],df))
        return _power(c,df,delta,p["tails"])-p["power"]
    if objective(4.0)>=0: return 4.0
    hi=4.0
    while hi<MAX_TOTAL:
        hi=min(MAX_TOTAL,hi*2)
        if objective(hi)>=0: break
    else: fail("NO_SOLUTION","power","No continuous solution within total search guard")
    if objective(hi)<0: fail("NO_SOLUTION","power","No continuous solution within total search guard")
    return float(brentq(objective,4.0,hi,xtol=1e-10,maxiter=300))


def analyze(data):
    p = _validate(data)
    global t, nct, brentq
    from scipy.stats import t, nct
    from scipy.optimize import brentq
    mode, tails = p["mode"], p["tails"]
    if mode == "a-priori":
        continuous = _continuous_total(p)
        n1,n2 = _allocate_total(_round_even_total(continuous),p["ratio"])
        if min(n1,n2)<2:
            fail("NO_SOLUTION", "ratio", "Final allocated groups fall below supported minimum 2")
        df,delta,_ = _base(n1,n2,p["d"])
        c=float(t.isf(p["alpha"]/tails,df))
        result={"ncp":delta,"critical_t":c,"df":df,"n1":n1,"n2":n2,"n_total":n1+n2,"actual_power":_power(c,df,delta,tails)}
        if any(isinstance(v,float) and not math.isfinite(v) for v in result.values()): fail("NO_SOLUTION",None,"Numerical result is not finite")
        return result
    df, delta, scale = _base(p["n1"], p["n2"], p.get("d", 1.0))
    if not math.isfinite(delta): fail("NO_SOLUTION", "d", "Noncentrality exceeds numerical range")
    c = float(t.isf(p.get("alpha", .05) / tails, df))
    if mode == "sensitivity":
        if p["power"] == p["alpha"]:
            return {"ncp": 0.0, "critical_t": c, "df": df, "d": 0.0}
        hi = 1.0
        while _power(c, df, hi, tails) < p["power"] and hi < MAX_DELTA: hi = min(MAX_DELTA, hi*2)
        if _power(c, df, hi, tails) < p["power"]: fail("NO_SOLUTION", "power", "No solution within noncentrality guard")
        delta = float(brentq(lambda x: _power(c, df, x, tails)-p["power"], 0, hi, xtol=1e-12))
        return {"ncp": delta, "critical_t": c, "df": df, "d": delta/scale}
    if mode in {"criterion", "compromise"}:
        def objective(x):
            power = _power(x, df, delta, tails)
            if mode == "criterion": return power-p["power"]
            alpha = float(t.sf(x, df))*tails
            return (1-power)-p["beta_alpha_ratio"]*alpha
        # Two-tailed threshold is nonnegative; one-tailed may be negative.
        low = 0.0 if tails == 2 else -1.0
        high = max(1.0, delta)
        while objective(low)*objective(high) > 0 and max(abs(low), high) < MAX_DELTA:
            if tails == 1: low *= 2
            high = min(MAX_DELTA, high*2)
        if objective(low)*objective(high) > 0: fail("NO_SOLUTION", "power" if mode == "criterion" else "beta_alpha_ratio", "No threshold within numerical guard")
        c = float(brentq(objective, low, high, xtol=1e-12))
    result = {"ncp": delta, "critical_t": c, "df": df}
    if mode == "post-hoc": result["power"] = _power(c, df, delta, tails)
    elif mode == "criterion": result["alpha"] = float(t.sf(c, df))*tails
    else:
        result["alpha"] = float(t.sf(c, df))*tails
        result["power"] = _power(c, df, delta, tails)
        result["beta"] = 1-result["power"]
    if any(isinstance(v, float) and not math.isfinite(v) for v in result.values()): fail("NO_SOLUTION", None, "Numerical result is not finite")
    return result
