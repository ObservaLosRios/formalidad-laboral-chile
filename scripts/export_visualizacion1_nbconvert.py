#!/usr/bin/env python3
"""Export Visualización 1 from the pipeline notebook to standalone HTML via nbconvert."""
from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
import plotly.graph_objects as go
import plotly.io as pio


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notebook",
        type=Path,
        default=Path("notebooks") / "pipeline_informalidad copy 2.ipynb",
        help="Absolute or relative path to the source notebook.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("graficosHTML") / "visualizacion1_tasa_informal_nbconvert.html",
        help="Destination HTML file path.",
    )
    return parser


def find_target_index(nb: nbformat.NotebookNode, marker: str) -> int:
    for idx, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", ""))
        if source.strip().startswith(marker):
            return idx
    raise ValueError(f"No se encontró la celda con marcador '{marker}'.")


def execute_notebook(nb: nbformat.NotebookNode, workdir: Path) -> nbformat.NotebookNode:
    executed = nbformat.v4.new_notebook()
    executed.metadata = nb.metadata
    executed.cells = [nbformat.from_dict(cell) for cell in nb.cells]

    kernel_name = nb.metadata.get("kernelspec", {}).get("name", "python3")
    executor = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)
    executor.preprocess(executed, resources={"metadata": {"path": str(workdir)}})
    return executed


def export_target_cell(executed_nb: nbformat.NotebookNode, target_idx: int, output_path: Path) -> None:
    target_cell = nbformat.from_dict(executed_nb.cells[target_idx])
    convert_plotly_output_to_html(target_cell)

    export_nb = nbformat.v4.new_notebook()
    export_nb.metadata = executed_nb.metadata
    export_nb.cells = [target_cell]

    exporter = HTMLExporter()
    exporter.exclude_input = True  # We only need the rendered output (chart)
    body, _ = exporter.from_notebook_node(export_nb)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(body, encoding="utf-8")


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    notebook_path = args.notebook.resolve()
    output_path = args.output.resolve()
    notebook_dir = notebook_path.parent

    nb = nbformat.read(notebook_path, as_version=4)
    marker = "# Visualización 1: Tasa de ocupación informal (%)"
    target_idx = find_target_index(nb, marker)

    executed_nb = execute_notebook(nb, notebook_dir)
    export_target_cell(executed_nb, target_idx, output_path)
    print(f"HTML exportado en: {output_path}")


def convert_plotly_output_to_html(cell: nbformat.NotebookNode) -> None:
    """Ensure Plotly mime outputs have an HTML fallback for nbconvert."""
    outputs = cell.get("outputs", [])
    for output in outputs:
        data = output.get("data")
        if not isinstance(data, dict):
            continue
        plotly_json = data.get("application/vnd.plotly.v1+json")
        if not plotly_json:
            continue
        fig = go.Figure(plotly_json)
        apply_hover_and_spike_style(fig)
        html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False)
        data["text/html"] = html


def apply_hover_and_spike_style(fig: go.Figure) -> None:
    """Standardize tooltip styling and vertical guide line behavior."""
    font_family = "Georgia, serif"
    tooltip_template = (
        "<span style='background-color:#ffffff;border:1px solid #333333;"
        "padding:6px 10px;display:inline-block;color:#000000;'>"
        "<b>%{x|%Y %b}</b><br>Tasa de ocupación informal (%): %{y:.1f}%"
        "</span><extra></extra>"
    )

    for trace in fig.data:
        trace_type = getattr(trace, "type", "")
        mode = getattr(trace, "mode", "") or ""
        x_values = getattr(trace, "x", []) or []
        if trace_type in {"scatter", "scattergl"} and "lines" in mode and len(x_values) > 1:
            trace.hovertemplate = tooltip_template

    fig.update_layout(
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#333333",
            font=dict(family=font_family, color="#000000"),
        ),
        hoverdistance=50,
    )

    fig.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikecolor="rgba(120, 120, 120, 0.6)",
        spikethickness=1.3,
        spikedash="solid",
    )
    fig.update_yaxes(showspikes=False)


if __name__ == "__main__":
    main()
