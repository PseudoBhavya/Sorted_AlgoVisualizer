"""
AlgoLens Code Panel Renderer
============================
Displays algorithm source code with line numbers, active execution pointer (>),
and cyan glow highlighting for the current instruction.
"""

from typing import List


class CodeHighlighter:
    """Renders formatted code view with active execution line pointer."""

    @classmethod
    def render_code_panel(cls, source_code: List[str], active_line: int = 1) -> str:
        """Render HTML code viewer matching the Stitch IDE design.
        
        Args:
            source_code: List of code lines (1-indexed matching)
            active_line: Currently executing line number
            
        Returns:
            HTML string
        """
        lines_html = []
        
        for idx, line in enumerate(source_code, start=1):
            is_active = (idx == active_line)
            
            if is_active:
                row_bg = "background: rgba(6, 182, 212, 0.12);"
                border_left = "border-left: 3px solid #06B6D4;"
                num_color = "#06B6D4"
                text_color = "#F8FAFC"
                chevron = '<span style="color: #06B6D4; font-weight: 800; margin-right: 6px; font-size: 11px;">▶</span>'
            else:
                row_bg = "background: transparent;"
                border_left = "border-left: 3px solid transparent;"
                num_color = "#475569"
                text_color = "#94A3B8"
                chevron = '<span style="display: inline-block; width: 14px;"></span>'

            # Clean and escape line
            safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # Indent spaces to non-breaking spaces
            leading_spaces = len(safe_line) - len(safe_line.lstrip(' '))
            spaced_line = ("&nbsp;" * leading_spaces) + safe_line.lstrip(' ')

            line_row = f"""
            <div style="display: flex; align-items: center; min-height: 22px; padding: 2px 8px; {row_bg} {border_left} font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 18px; box-sizing: border-box;">
                <span style="display: inline-block; width: 28px; text-align: right; color: {num_color}; font-weight: 500; margin-right: 12px; user-select: none;">{idx}</span>
                {chevron}
                <span style="color: {text_color}; white-space: pre-wrap; font-family: 'JetBrains Mono', monospace;">{spaced_line}</span>
            </div>
            """
            lines_html.append(line_row)

        return f"""
        <div style="background: #0B0F17; border: 1px solid #1F2937; border-radius: 8px; overflow: hidden; width: 100%; box-sizing: border-box;">
            <div style="background: #111827; border-bottom: 1px solid #1F2937; padding: 6px 12px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #EF4444;"></span>
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #F59E0B;"></span>
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #10B981;"></span>
                    <span style="color: #94A3B8; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-left: 8px;">source.py</span>
                </div>
                <span style="color: #06B6D4; font-family: 'JetBrains Mono', monospace; font-size: 11px;">Line {active_line}</span>
            </div>
            <div style="padding: 6px 0; overflow-x: auto; max-height: 380px;">
                {"".join(lines_html)}
            </div>
        </div>
        """
