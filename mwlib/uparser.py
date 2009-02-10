import os
if "MWREFINE" in os.environ:
    import sys
    sys.stderr.write("USING NEW REFINE PARSER\n")
    from mwlib.refine.uparser import simpleparse, parseString
else:
    from mwlib.old_uparser import simpleparse, parseString
