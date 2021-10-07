# Issue Template

## Python version

- *Please run the following snippet and write the output here*

```python {.line-numbers}
import platform
import sys
from pprint import pprint

pprint("python=" + sys.version)
pprint("os=" + platform.platform())

try:
    import numpy
    pprint("numpy=" + numpy.__version__)
except ImportError:
    pass

try:
    import openGA
    pprint("openGA=" + openGA.__version__)
except ImportError:
    pass
```

## Code

### Code snippet

- *please write here the code snippet that triggers the error*
  
### Traceback

- *please write here the error traceback*
  
## Description

The fastest way to debug is to have the original file. For data protection you can use the static
method _scramble_ to scramble all text blocks, and send the scrambled file by e-mail.

- *please describe the issue here*
