# S23 activation conditions

S23 may become an upload candidate only when both inputs are positive:

1. S22 scores at least 90, or its isolated result otherwise establishes a
   credible frame gain over the frozen 88.155 S18 control.
2. V19/S19 is classified `tail-positive` under T7 using its exact scored hash.

If either condition fails or remains pending, keep S23 frozen and do not upload
it. A local pass proves source lineage, prefix preservation, and packaging; it
does not replace either hosted result.

When activated, verify that S23's diff is exactly the union of:

- S18→S22: the two extra frame constants and five-frame tuple, plus comments;
- S18→S19: the 64-tail constant, cap clamp, and eligible-cutoff append.

No replay-fraction, fill, selector, multipost, burst, fallback, or notebook-gate
change is allowed.
