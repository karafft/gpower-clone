"""Read-only PE string/xref evidence collector. No decompilation or execution.

Optional dependency: capstone>=5,<6. Original executable stays outside delivery.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct


NEEDLES = [
    b"Power must be greater than or equal to alpha.",
    b"The allocation ratio falls outside",
    b"In an a priori analysis, the absolute value of the",
    b"Means: Difference between two independent means (two groups)",
    b"Alpha is outside the admissible range (",
    b"Total sample size is outside the admissible range (",
    b"Power is outside the admissible range (",
]


def inspect(binary):
    import capstone
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_MODE_64
    data = binary.read_bytes()
    if data[:2] != b"MZ":
        raise ValueError("Expected Windows PE executable")
    pe = struct.unpack_from("<I", data, 0x3c)[0]
    if data[pe:pe+4] != b"PE\0\0":
        raise ValueError("PE signature missing")
    machine, count = struct.unpack_from("<HH", data, pe+4)
    size = struct.unpack_from("<H", data, pe+20)[0]
    optional = pe+24
    magic = struct.unpack_from("<H", data, optional)[0]
    if magic == 0x10b:
        base = struct.unpack_from("<I", data, optional+28)[0]
        mode = CS_MODE_32
    elif magic == 0x20b:
        base = struct.unpack_from("<Q", data, optional+24)[0]
        mode = CS_MODE_64
    else:
        raise ValueError("Unsupported PE optional header")
    sections = []
    for i in range(count):
        off = optional+size+i*40
        name = data[off:off+8].rstrip(b"\0").decode("ascii", errors="replace")
        virtual_size, rva, raw_size, raw = struct.unpack_from("<IIII", data, off+8)
        flags = struct.unpack_from("<I", data, off+36)[0]
        sections.append(dict(name=name, rva=rva, raw=raw, raw_size=raw_size,
                             virtual_size=virtual_size, executable=bool(flags & 0x20000000)))
    findings = []
    for needle in NEEDLES:
        start = 0
        while True:
            pos = data.find(needle, start)
            if pos < 0:
                break
            section = next((s for s in sections if s["raw"] <= pos < s["raw"]+s["raw_size"]), None)
            if section:
                rva = section["rva"]+pos-section["raw"]
                findings.append(dict(id=f"REA-STATIC-{len(findings)+1:03d}",
                    text=needle.decode(), file_offset=hex(pos), rva=hex(rva),
                    preferred_va=hex(base+rva), section=section["name"], code_references=[]))
            start = pos+len(needle)
    by_va = {int(f["preferred_va"], 16): f for f in findings}
    decoder = Cs(CS_ARCH_X86, mode)
    decoder.skipdata = True
    for section in sections:
        if not section["executable"]:
            continue
        raw = section["raw"]
        for address, length, mnemonic, operands in decoder.disasm_lite(
                data[raw:raw+section["raw_size"]], base+section["rva"]):
            # Static preferred-image absolute references only; no dynamic tracing.
            values = set(int(x, 16) for x in re.findall(r"0x[0-9a-fA-F]+", operands))
            for target in values & by_va.keys():
                by_va[target]["code_references"].append(dict(preferred_va=hex(address),
                    file_offset=hex(raw+address-base-section["rva"]), instruction=mnemonic+" "+operands))
    digest = hashlib.sha256(data).hexdigest()
    anchors = None
    if digest == "c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812":
        def va_offset(va):
            rva = va-base
            s = next(s for s in sections if s["rva"] <= rva < s["rva"]+s["raw_size"])
            return s["raw"]+rva-s["rva"]
        threshold = struct.unpack_from("<d", data, va_offset(0x5c7ed8))[0]
        validator = struct.unpack_from("<I", data, va_offset(0x5ca40c+0x104))[0]
        label_path = struct.unpack_from("<I", data, va_offset(0x5ca40c+0x78))[0]
        branch_off = va_offset(0x4d9285)
        instruction = next(decoder.disasm_lite(data[branch_off:branch_off+6], 0x4d9285))
        anchors = dict(applicable_only_to_sha256=digest,
            constant_va="0x5c7ed8", absolute_effect_threshold=threshold,
            table_va="0x5ca40c", validator_slot="0x104", validator_va=hex(validator),
            label_slot="0x78", label_path_va=hex(label_path),
            acceptance_branch_va=hex(instruction[0]),
            acceptance_branch=instruction[2]+" "+instruction[3],
            alpha_power_bounds={"minimum": struct.unpack_from("<d", data, va_offset(0x5c4398))[0],
                                "maximum": struct.unpack_from("<d", data, va_offset(0x5c6860))[0],
                                "minimum_constant_va": "0x5c4398", "maximum_constant_va": "0x5c6860",
                                "alpha_validator_va": "0x487460", "power_validator_va": "0x488010",
                                "comparison": "strict-below/above reject branches; endpoints accepted"},
            allocation_bounds={"minimum": struct.unpack_from("<d", data, va_offset(0x5c3b50))[0],
                               "maximum": 1.0/struct.unpack_from("<d", data, va_offset(0x5c3b50))[0],
                               "minimum_constant_va": "0x5c3b50", "t2_indep_callsite_va": "0x4d9c3c",
                               "validator_va": "0x487300", "comparison": "inclusive bounds"},
            allocation_pipeline={
                "solver_vtable_slot": "0x48",
                "solver_wrapper_va": hex(struct.unpack_from("<I", data, va_offset(0x5ca40c+0x48))[0]),
                "rounding_vtable_slot": "0x74",
                "rounding_wrapper_va": hex(struct.unpack_from("<I", data, va_offset(0x5ca40c+0x74))[0]),
                "preceil_scale_va": "0x5c4328",
                "preceil_scale": struct.unpack_from("<d", data, va_offset(0x5c4328))[0],
                "solver_tolerance_va": "0x5c3f48",
                "solver_tolerance_argument": struct.unpack_from("<d", data, va_offset(0x5c3f48))[0],
                "near_equal_tolerance_va": "0x5c4198",
                "near_equal_tolerance": struct.unpack_from("<d", data, va_offset(0x5c4198))[0],
                "first_group_round_call_va": "0x4d9d55", "second_group_ceil_call_va": "0x4d9d88",
                "final_power_call_va": "0x4d9e3c", "return_va": "0x4d9e4c",
                "floor_thunk_va": "0x5ac023", "floor_iat_va": "0x5be5b8",
                "ceil_thunk_va": "0x5ac047", "ceil_iat_va": "0x5be590",
                "semantics_source": "docs/REA_STATIC_FINDINGS.md REA-STATIC-008/009"},
            status="Static anchors confirmed; semantic interpretation in docs/REA_STATIC_FINDINGS.md")
    return dict(binary_name=binary.name, sha256=digest,
                bytes=len(data), pe_machine=hex(machine), image_base=hex(base),
                method=f"Read-only PE parsing and Capstone {capstone.__version__} static instruction references",
                limitations="Preferred image addresses; ASLR may relocate. No executable run, GUI, Ghidra, decompiler, or control-flow proof. String xrefs alone do not establish test-specific algorithm semantics.",
                findings=findings, known_binary_anchors=anchors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dict(findings=len(result["findings"]),
                         referenced=sum(bool(f["code_references"]) for f in result["findings"]),
                         sha256=result["sha256"])))


if __name__ == "__main__":
    main()
