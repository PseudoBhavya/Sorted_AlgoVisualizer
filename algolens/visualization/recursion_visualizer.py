"""
AlgoLens Recursion & Call Stack Visualizer
==========================================
Renders call stack frames and divide-and-conquer call tree for recursive algorithms
like QuickSort and MergeSort.
"""

from typing import List, Dict, Any, Optional


class RecursionVisualizer:
    """Renders visual call stack frames and recursion tree nodes."""

    @classmethod
    def render_call_stack(cls, recursion_state: Optional[Dict[str, Any]], max_depth: int = 1) -> str:
        """Render the active call stack frames drawer."""
        if not recursion_state:
            return """
            <div style="background: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 10px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #475569;">
                No active recursive call frame (Iterative scope).
            </div>
            """

        depth = recursion_state.get('depth', 0)
        call = recursion_state.get('call', 'root()')
        parent = recursion_state.get('parent', 'None')

        frames = []
        # Parent frame (inactive/waiting)
        if parent and parent != "None":
            frames.append(f"""
            <div style="background: #1E293B; border-left: 3px solid #6366F1; padding: 6px 10px; border-radius: 4px; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;">{parent}</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #6366F1; background: rgba(99, 102, 241, 0.1); padding: 1px 6px; border-radius: 3px;">WAITING</span>
            </div>
            """)

        # Current frame (active)
        frames.append(f"""
        <div style="background: rgba(99, 102, 241, 0.2); border-left: 3px solid #06B6D4; padding: 6px 10px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; color: #F8FAFC;">{call}</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; color: #06B6D4; background: rgba(6, 182, 212, 0.2); padding: 1px 6px; border-radius: 3px;">ACTIVE (Depth {depth})</span>
        </div>
        """)

        return f"""
        <div style="background: #0F172A; border: 1px solid #1F2937; border-radius: 8px; overflow: hidden; width: 100%; box-sizing: border-box;">
            <div style="background: #111827; padding: 6px 10px; border-bottom: 1px solid #1F2937; display: flex; align-items: center; justify-content: space-between;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; color: #6366F1; text-transform: uppercase;">Call Stack Frame</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94A3B8;">Max Depth: {max_depth}</span>
            </div>
            <div style="padding: 8px;">
                {"".join(frames)}
            </div>
        </div>
        """
