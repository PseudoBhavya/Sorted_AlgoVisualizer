"""
AlgoLens State & Explanation Renderer
======================================
Renders pedagogical state cards, invariant checks, variable inspection tables,
and execution metrics matching the Stitch design.
"""

from typing import Dict, Any
from algolens.algorithms.steps import AlgorithmStep


class StateRenderer:
    """Renders state inspector, pedagogical explanation, and variable tables."""

    @classmethod
    def render_explanation_card(cls, step: AlgorithmStep) -> str:
        """Render the 'Why this step?' pedagogical explanation card."""
        op_color = "#06B6D4"
        if step.operation in ("SWAP", "VIOLATION"):
            op_color = "#F43F5E"
        elif step.operation in ("PIVOT_SELECT", "PARTITION"):
            op_color = "#F59E0B"
        elif step.operation in ("FOUND", "COMPLETE"):
            op_color = "#10B981"

        return f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 12px; margin-bottom: 12px; box-sizing: border-box;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 14px;">💡</span>
                    <span style="font-family: 'Geist', sans-serif; font-size: 13px; font-weight: 600; color: #F8FAFC;">Step Explanation</span>
                </div>
                <span style="background: rgba(6, 182, 212, 0.15); color: {op_color}; border: 1px solid {op_color}; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">
                    {step.operation}
                </span>
            </div>
            <p style="font-family: 'Geist', sans-serif; font-size: 13px; line-height: 20px; color: #DCE2F7; margin: 0;">
                {step.explanation or "Executing current instruction..."}
            </p>
        </div>
        """

    @classmethod
    def render_variables_table(cls, step: AlgorithmStep) -> str:
        """Render Memory Watch / Variables Inspection table."""
        vars_dict = dict(step.variables)
        # Merge pointers into variables for clear inspection
        for p_name, p_val in step.pointers.items():
            vars_dict[f"ptr_{p_name}"] = p_val
            
        if step.pivot:
            vars_dict["pivot_val"] = step.pivot.get('value')
            vars_dict["pivot_idx"] = step.pivot.get('index')

        if not vars_dict:
            return '<div style="color: #475569; font-size: 12px; padding: 8px;">No active variables</div>'

        rows = []
        for k, v in vars_dict.items():
            rows.append(f"""
            <tr style="border-bottom: 1px solid #1F2937;">
                <td style="padding: 4px 8px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #06B6D4;">{k}</td>
                <td style="padding: 4px 8px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #F8FAFC; text-align: right; font-weight: 600;">{v}</td>
            </tr>
            """)

        return f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; overflow: hidden; width: 100%; box-sizing: border-box;">
            <div style="background: #0F172A; padding: 6px 10px; border-bottom: 1px solid #1F2937; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; color: #94A3B8; text-transform: uppercase;">Variable Watch</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #475569;">Scope: Local</span>
            </div>
            <div style="max-height: 180px; overflow-y: auto;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tbody>
                        {"".join(rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """

    @classmethod
    def render_metrics_deck(cls, step: AlgorithmStep, total_steps: int) -> str:
        """Render running metrics counters deck."""
        metrics = step.metrics or {}
        comps = metrics.get('comparisons', 0)
        swaps = metrics.get('swaps', 0)
        depth = metrics.get('recursion_depth', 0)
        cur_step = step.step_number

        return f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px;">
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 8px; text-align: center;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94A3B8; text-transform: uppercase;">Step</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: #06B6D4;">{cur_step} <span style="font-size: 11px; color: #475569;">/ {total_steps}</span></div>
            </div>
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 8px; text-align: center;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94A3B8; text-transform: uppercase;">Comparisons</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: #F8FAFC;">{comps}</div>
            </div>
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 8px; text-align: center;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94A3B8; text-transform: uppercase;">Swaps</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: #F43F5E;">{swaps}</div>
            </div>
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 8px; text-align: center;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94A3B8; text-transform: uppercase;">Recursion Depth</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: #6366F1;">{depth}</div>
            </div>
        </div>
        """
