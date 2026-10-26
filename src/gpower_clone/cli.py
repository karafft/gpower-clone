import sys
from .engine import analyze, AnalysisError, VERSION, serialize

def parse(argv):
    if argv == ["--version"]: return None
    data = {}
    index = 0
    while index < len(argv):
        token = argv[index]
        if not token.startswith("--") or token == "--":
            raise AnalysisError("UNKNOWN_PARAM", token, "Expected named parameter")
        field = token[2:]
        if field in data: raise AnalysisError("INVALID_VALUE", field, "Duplicate parameter")
        if index+1 == len(argv) or argv[index+1].startswith("--"):
            raise AnalysisError("MISSING_PARAM", field, "Parameter value missing")
        data[field] = argv[index+1]
        index += 2
    return data

def main(argv=None):
    try:
        params = parse(sys.argv[1:] if argv is None else argv)
        result = VERSION if params is None else analyze(params)
        status = 0
    except AnalysisError as exc:
        result, status = exc.as_dict(), 2
    except Exception:
        result, status = {"error": "Internal numerical or runtime error", "code": "INTERNAL_ERROR", "field": None}, 1
    print(serialize(result))
    return status
