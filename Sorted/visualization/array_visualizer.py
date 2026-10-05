"""
AlgoLens Array Visualizer Component
===================================
Renders pixel-perfect HTML/SVG array visualizations strictly matching the Stitch design system.
Includes:
- Dynamic proportional bar heights
- Pivot highlight (amber #F59E0B with floating badge)
- Swap violation highlights (crimson #F43F5E with pulsing glow & violation tags)
- Comparing active elements (cyan #06B6D4)
- Sorted elements (emerald #10B981)
- Curved SVG Swap Arc with badge
- Partition / Subarray bounding indicator
- Pointers and index pills in JetBrains Mono
"""

from typing import Optional, List
try:
    from Sorted.algorithms.steps import AlgorithmStep
except ImportError:
    from algolens.algorithms.steps import AlgorithmStep


class ArrayVisualizer:
    """Renders HTML/SVG visualization for an AlgorithmStep."""

    @classmethod
    def render_step_html(cls, step: AlgorithmStep, max_val_override: Optional[float] = None) -> str:
        """Render complete HTML visualizer stage for the given step."""
        arr = step.array_state
        n = len(arr)
        if n == 0:
            return '<div style="color: #94A3B8; text-align: center; padding: 40px;">Empty Array</div>'

        # Compute scaling
        numeric_vals = [float(x) for x in arr]
        max_v = max_val_override if max_val_override is not None else max(max(numeric_vals), 1.0)
        min_v = min(numeric_vals)

        # Detect special states
        pivot_idx = step.pivot.get('index') if step.pivot else None
        active_indices = set(step.active_indices or [])
        sorted_indices = set(step.sorted_indices or [])
        
        swap_a = step.swap.get('index_a') if step.swap else None
        swap_b = step.swap.get('index_b') if step.swap else None

        comp_left = step.comparison.get('left_index') if step.comparison else None
        comp_right = step.comparison.get('right_index') if step.comparison else None

        pointers = step.pointers or {}
        
        # Partition bounds
        part_low = step.partition_range.get('low') if step.partition_range else 0
        part_high = step.partition_range.get('high') if step.partition_range else n - 1

        # Search range (for binary search)
        search_low = step.search_range.get('low') if step.search_range else None
        search_mid = step.search_range.get('mid') if step.search_range else None
        search_high = step.search_range.get('high') if step.search_range else None

        # Build Swap Arc SVG if a swap is occurring
        swap_svg = ""
        if swap_a is not None and swap_b is not None and swap_a != swap_b and n > 1:
            left_pos = min(swap_a, swap_b)
            right_pos = max(swap_a, swap_b)
            
            # Estimate percentages
            p1_pct = ((left_pos + 0.5) / n) * 100.0
            p2_pct = ((right_pos + 0.5) / n) * 100.0
            mid_pct = (p1_pct + p2_pct) / 2.0
            
            swap_svg = f"""
            <div style="position: relative; width: 100%; height: 50px; pointer-events: none; margin-bottom: -10px; z-index: 10;">
                <svg style="width: 100%; height: 100%; overflow: visible;" viewBox="0 0 1000 60" preserveAspectRatio="none">
                    <path d="M {p1_pct * 10} 55 Q {mid_pct * 10} -15 {p2_pct * 10} 55"
                          fill="none" stroke="#F43F5E" stroke-width="2.5" stroke-dasharray="6,4"
                          style="animation: pulse 1.5s infinite;" />
                    <g transform="translate({mid_pct * 10}, 14)">
                        <rect x="-38" y="-12" width="76" height="24" rx="12" fill="#93000A" stroke="#FFDAD6" stroke-width="1.2" />
                        <text x="0" y="4.5" fill="#FFDAD6" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" text-anchor="middle">⇄ SWAP</text>
                    </g>
                </svg>
            </div>
            """

        # Generate each bar's HTML
        bars_html = []
        for i, val in enumerate(arr):
            # Calculate height percentage (min 15% for visibility, max 95%)
            if max_v > 0:
                h_pct = max(15.0, min(95.0, (float(val) / max_v) * 92.0))
            else:
                h_pct = 20.0

            # Determine styling role
            is_pivot = (i == pivot_idx)
            is_swapping = (i == swap_a or i == swap_b)
            is_comparing = (i == comp_left or i == comp_right or (i in active_indices and not is_swapping and not is_pivot))
            is_sorted = (i in sorted_indices)
            is_found = (step.operation == 'FOUND' and i in active_indices)
            
            # Check if out of binary search range
            is_eliminated = False
            if search_low is not None and search_high is not None:
                if i < search_low or i > search_high:
                    is_eliminated = True

            # Pointer labels for this bar
            bar_pointers = []
            for p_name, p_idx in pointers.items():
                if p_idx == i:
                    bar_pointers.append(p_name)
            
            # Badges above bar
            top_badge = ""
            if is_pivot:
                top_badge = """
                <div style="padding: 2px 7px; border-radius: 9999px; background: #E79400; color: #563400;
                            font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 800;
                            letter-spacing: 0.05em; display: flex; align-items: center; gap: 2px;
                            box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); margin-bottom: 4px;">
                    🚩 PIVOT
                </div>
                """
            elif is_swapping:
                tag = "i" if i == swap_a else "j"
                top_badge = f"""
                <div style="padding: 2px 6px; border-radius: 4px; background: #93000A; color: #FFDAD6;
                            font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
                            box-shadow: 0 0 12px rgba(244, 63, 94, 0.5); margin-bottom: 4px;">
                    {tag}↓
                </div>
                """
            elif is_found:
                top_badge = """
                <div style="padding: 2px 6px; border-radius: 4px; background: #065F46; color: #A7F3D0;
                            font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
                            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5); margin-bottom: 4px;">
                    MATCH!
                </div>
                """
            elif search_mid is not None and i == search_mid:
                top_badge = """
                <div style="padding: 2px 6px; border-radius: 4px; background: #003640; color: #4CD7F6;
                            font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;
                            border: 1px solid #06B6D4; margin-bottom: 4px;">
                    MID
                </div>
                """
            else:
                top_badge = '<div style="height: 18px;"></div>'

            # Bar background and border colors
            if is_found:
                bar_bg = "linear-gradient(to top, #047857, #10B981)"
                bar_border = "#10B981"
                text_color = "#FFFFFF"
                bar_shadow = "0 0 16px rgba(16, 185, 129, 0.6)"
            elif is_pivot:
                bar_bg = "linear-gradient(to top, rgba(245, 158, 11, 0.3), #F59E0B)"
                bar_border = "#F59E0B"
                text_color = "#0C1322"
                bar_shadow = "0 0 14px rgba(245, 158, 11, 0.4)"
            elif is_swapping:
                bar_bg = "linear-gradient(to top, #93000A, #F43F5E)"
                bar_border = "#FFB4AB"
                text_color = "#FFFFFF"
                bar_shadow = "0 0 18px rgba(244, 63, 94, 0.6)"
            elif is_comparing:
                bar_bg = "linear-gradient(to top, #00424F, #06B6D4)"
                bar_border = "#4CD7F6"
                text_color = "#FFFFFF"
                bar_shadow = "0 0 14px rgba(6, 182, 212, 0.45)"
            elif is_sorted:
                bar_bg = "linear-gradient(to top, #064E3B, #059669)"
                bar_border = "#10B981"
                text_color = "#DCE2F7"
                bar_shadow = "none"
            elif is_eliminated:
                bar_bg = "#191F2F"
                bar_border = "#232A3A"
                text_color = "#475569"
                bar_shadow = "none"
            else:
                bar_bg = "#232A3A"
                bar_border = "#374151"
                text_color = "#BCC9CD"
                bar_shadow = "none"

            opacity = "0.35" if is_eliminated else "1.0"

            # Pointer string below
            ptr_str = " • ".join(bar_pointers) if bar_pointers else ("" if not is_pivot else "pivot")
            ptr_color = "#F59E0B" if is_pivot else ("#F43F5E" if is_swapping else "#4CD7F6")

            bar_cell = f"""
            <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%; opacity: {opacity}; transition: all 0.25s ease;">
                {top_badge}
                <div style="width: 100%; height: {h_pct}%; border-radius: 4px 4px 0 0; background: {bar_bg}; border: 1.5px solid {bar_border}; box-shadow: {bar_shadow}; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding-top: 6px; box-sizing: border-box;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; color: {text_color}; text-shadow: 0 1px 2px rgba(0,0,0,0.6);">{val}</span>
                </div>
                <div style="margin-top: 4px; padding: 2px 5px; border-radius: 3px; background: #141B2B; border: 1px solid #232A3A; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: {text_color};">
                    [{i}]
                </div>
                <div style="height: 14px; margin-top: 2px; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 600; color: {ptr_color}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {ptr_str}
                </div>
            </div>
            """
            bars_html.append(bar_cell)

        # Active Partition / Invariant banner
        partition_banner = ""
        if step.partition_range:
            low = step.partition_range.get('low', 0)
            high = step.partition_range.get('high', n - 1)
            p_val = step.pivot.get('value', '—') if step.pivot else '—'
            partition_banner = f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 12px; background: #141B2B; border: 1px solid #232A3A; border-radius: 8px; margin-bottom: 12px; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #4CD7F6; font-weight: 600;">Subarray Scope:</span>
                    <span style="background: #191F2F; padding: 2px 8px; border-radius: 4px; color: #F8FAFC; border: 1px solid #374151;">arr[{low} .. {high}]</span>
                    <span style="color: #869397;">|</span>
                    <span style="color: #FFB95F;">Pivot = {p_val}</span>
                </div>
                <div style="color: #94A3B8; font-size: 11px;">
                    Operation: <span style="color: #4CD7F6; font-weight: 600;">{step.operation}</span>
                </div>
            </div>
            """

        container_html = f"""
        <div style="width: 100%; background: #0C1322; border: 1px solid #1F2937; border-radius: 12px; padding: 16px; box-sizing: border-box; display: flex; flex-direction: column;">
            {partition_banner}
            {swap_svg}
            <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 6px; height: 240px; padding: 8px 4px; background: #0F172A; border-radius: 8px; border: 1px solid #1E293B;">
                {"".join(bars_html)}
            </div>
        </div>
        """
        return container_html
