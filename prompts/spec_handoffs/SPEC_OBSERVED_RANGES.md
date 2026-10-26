# Final clean domain range specification from separate static analysis

CONTRACT allows broad positive inputs but says interior rejection must follow observed behavior. Separate binary analysis has now established these more specific bounds. Do not inspect raw evidence, executable, or parent reports; implement only these semantic rules.

- For any supplied alpha or power field, require inclusive1e-7<=value<=0.9999999 in addition to existing CONTRACT finite/type validation. OUT_OF_RANGE with that field when outside. Test exact endpoints and math.nextafter neighbors, not approximate rounded comparisons.
- A-priori ratio inclusive0.01<=ratio<=100.0. OUT_OF_RANGE field ratio outside. Other modes reject ratio as irrelevant as before.
- These are separately analyzed domain constraints (source labels REA-STATIC-002/005 and same analyzed power validator), not arbitrary engineering guards. Original a-priori d>=1e-5 and nonnegative sensitivity result remain.
- Version1.1.0rc3 consistently. Add meaningful bound regression cases; keep ordinary public, inverse, even-total minimality, MCP parity and installed CLI checks. Parent will do the final external source suite. No new features needed; no raw-source access, no ZIP, no repo write.
