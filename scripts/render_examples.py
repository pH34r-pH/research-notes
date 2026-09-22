#!/usr/bin/env python3
"""Refresh saved teaching outputs; this does not qualify historical evidence."""
import importlib.metadata
import subprocess
import sys
from pathlib import Path

import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

root = Path(__file__).resolve().parents[1]
versions = {name: importlib.metadata.version(name) for name in ('numpy', 'matplotlib', 'scikit-learn')}
if len(sys.argv) == 1:
    for path in sorted((root / 'notebooks').glob('*.ipynb')):
        subprocess.run([sys.executable, __file__, str(path)], check=True, timeout=180)
    sys.exit(0)

for path in [Path(sys.argv[1])]:
    notebook = nbformat.read(path, as_version=4)
    if notebook.metadata.get('publication', {}).get('exampleKind') != 'illustrative':
        raise ValueError(f'{path.name}: execution requires an explicit illustrative-example boundary')
    # A fresh IPython process per notebook captures display outputs without a
    # network kernel. Only these explicitly labelled, trusted examples execute.
    shell = InteractiveShell.instance()
    shell.run_cell("import matplotlib; matplotlib.use('module://matplotlib_inline.backend_inline')")
    count = 0
    for cell in notebook.cells:
        cell.metadata.pop('execution', None)
        if cell.cell_type != 'code':
            continue
        count += 1
        with capture_output() as captured:
            result = shell.run_cell(cell.source)
        if not result.success:
            raise RuntimeError(f'{path.name}: {result.error_before_exec or result.error_in_exec}')
        cell.execution_count = count
        cell.outputs = []
        for name, value in [('stdout', captured.stdout), ('stderr', captured.stderr)]:
            if value:
                cell.outputs.append(nbformat.v4.new_output('stream', name=name, text=value))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
        descriptions = iter(cell.metadata.get('publication', {}).get('outputAlt', []))
        for output in cell.get('outputs', []):
            if 'image/png' in output.get('data', {}):
                description = next(descriptions, None)
                if not description:
                    raise ValueError(f'{path.name}: every plot needs a source-authored description')
                output.setdefault('metadata', {})['publication'] = {'alt': description}
    notebook.metadata.publication['outputEnvironment'] = versions
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    print(f'Rendered illustrative outputs: {path.name}', flush=True)
