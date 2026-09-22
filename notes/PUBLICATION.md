# Publishing the teaching examples

The milestone notebooks narrate the research. Their small runnable cells are
illustrative examples, as required by the chronology's publication boundary.
Saved output lets a reader inspect those examples without opening a kernel;
it is not a benchmark replay or a qualification receipt.

To refresh the outputs from this repository:

```sh
python -m pip install -r requirements.txt
python scripts/render_examples.py
```

The script runs each trusted notebook in a fresh IPython process and records
the NumPy, Matplotlib, and scikit-learn versions in notebook metadata. Seeds
belong in the examples. Small numerical differences across environments do
not change these outputs into historical measurements.

Each notebook's `metadata.publication` supplies its research `question`,
milestone `sequence` where applicable, and `exampleKind: illustrative`.
Portfolio consumes these authored fields. A checkout timestamp is not a
research date. Plot cells also supply `metadata.publication.outputAlt`, one
description per image, which the renderer attaches to the saved output.

Public formal-source links are pinned to a reviewed theorem-library revision.
The formal assumptions and conclusions remain in that repository. The public
account of milestone 013 explicitly distinguishes the historical benchmark
from its synthetic logistic-probe example; no exact replay is published here.
