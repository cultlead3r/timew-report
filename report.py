import sys
import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Generate time tracking reports')
parser.add_argument('--format', choices=['html', 'pdf'], default='html', help='Output format (default: html)')
args = parser.parse_args()

data = sys.stdin.read()
intervals = json.loads(data)

# SVG Logo (for cyberpunk/HTML - white and cyan)
logo_svg_cyberpunk = '''<svg id="Layer_2" xmlns="http://www.w3.org/2000/svg" height="36px" viewBox="0 0 390.96 67.3" preserveAspectRatio="XMidYMid meet">
  <defs>
    <style>
      .cls-1 { fill: #fff; }
      .cls-2 { fill: #49dbe5; }
    </style>
  </defs>
  <g id="Layer_1-2">
    <g>
      <g>
        <path class="cls-1" d="M193.21,10.63L198.41,.14c.04-.09,.13-.14,.22-.14h64.33c.19,0,.31,.2,.22,.36l-4.78,9.6c-.32,.64-.96,1.03-1.67,1.03h-63.31c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-2" d="M190.69,15.71l1.44-2.9c.04-.09,.13-.14,.22-.14h64.39c1.35,0,2.56-.75,3.16-1.96L265.17,.14c.04-.08,.13-.14,.22-.14h3.46c.18,0,.31,.19,.22,.36l-6.51,13.38c-.91,1.56-2.13,2.33-3.73,2.33h-67.91c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-1" d="M122.66,16.07c-.14,0-.25-.11-.25-.25V.25c0-.14,.11-.25,.25-.25h15.92c.19,0,.31,.19,.22,.36l-7.71,15.57c-.04,.09-.13,.14-.22,.14h-8.2Z" />
        <path class="cls-2" d="M171.65,6.34l3.07-6.2c.04-.09,.13-.14,.22-.14h6.06c.19,0,.31,.19,.22,.36l-4.86,9.81c-.07,.15-.26,.18-.39,.08l-4.27-3.61c-.09-.07-.11-.2-.06-.3Z" />
        <path class="cls-2" d="M150.04,15.71l3.65-7.36c.07-.15,.26-.18,.39-.08l4.27,3.61c.09,.07,.11,.2,.06,.3l-1.86,3.76c-.04,.09-.13,.14-.22,.14h-6.06c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-2" d="M133.07,15.71l3.65-7.36c.07-.15,.26-.18,.39-.08l4.27,3.61c.09,.07,.11,.2,.06,.3l-1.86,3.76c-.04,.09-.13,.14-.22,.14h-6.06c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-2" d="M158.52,15.71l3.65-7.36c.07-.15,.26-.18,.39-.08l4.27,3.61c.09,.07,.11,.2,.06,.3l-1.86,3.76c-.04,.09-.13,.14-.22,.14h-6.06c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-2" d="M167.01,15.71l3.65-7.36c.07-.15,.26-.18,.39-.08l4.27,3.61c.09,.07,.11,.2,.06,.3l-1.86,3.76c-.04,.09-.13,.14-.22-.14h-6.06c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-2" d="M141.55,15.71l3.65-7.36c.07-.15,.26-.18,.39-.08l4.27,3.61c.09,.07,.11,.2,.06,.3l-1.86,3.76c-.04,.09-.13,.14-.22,.14h-6.06c-.19,0-.31-.19-.22-.36Z" />
        <path class="cls-2" d="M163.16,6.34l3.07-6.2c.04-.09,.13-.14,.22-.14h6.06c.19,0,.31,.19,.22,.36l-4.86,9.81c-.07,.15-.26,.18-.39,.08l-4.27-3.61c-.09-.07-.11-.2-.06-.3Z" />
        <path class="cls-2" d="M137.71,6.34l3.07-6.2c.04-.09,.13-.14,.22-.14h6.06c.19,0,.31,.19,.22,.36l-4.86,9.81c-.07,.15-.26,.18-.39,.08l-4.27-3.61c-.09-.07-.11-.2-.06-.3Z" />
        <path class="cls-2" d="M154.68,6.34l3.07-6.2c.04-.09,.13-.14,.22-.14h6.06c.19,0,.31,.19,.22,.36l-4.86,9.81c-.07,.15-.26,.18-.39,.08l-4.27-3.61c-.09-.07-.11-.2-.06-.3Z" />
        <path class="cls-2" d="M146.2,6.34l3.07-6.2c.04-.09,.13-.14,.22-.14h6.06c.19,0,.31,.19,.22,.36l-4.86,9.81c-.07,.15-.26,.18-.39,.08l-4.27-3.61c-.09-.07-.11-.2-.06-.3Z" />
        <path class="cls-1" d="M175.49,15.71L183.2,.14c.04-.09,.13-.14,.22-.14h10.52c.19,0,.31,.19,.22,.36l-7.71,15.57c-.04,.09-.13,.14-.22,.14h-10.52c-.19,0-.31-.19-.22-.36Z" />
      </g>
      <g>
        <path class="cls-2" d="M53.13,45.36v12.66c0,2.56-.92,4.75-2.77,6.56-1.84,1.81-4.07,2.72-6.67,2.72H8.82l-.18-.08-.07-.17v-18.5l.07-.17,.18-.08h7.21l.18,.08,.07,.17v12h27.41c.48,0,.89-.17,1.22-.5s.5-.73,.5-1.19v-14.37c0-.46-.17-.86-.5-1.19s-.74-.5-1.22-.5H.25l-.17-.06-.08-.19v-6.25l.08-.17,.17-.08H43.69c2.6,0,4.83,.9,6.67,2.72,1.85,1.81,2.77,4.01,2.77,6.59Zm52.95,21.5l-28.84-28.34c-1.75-1.65-3.78-2.47-6.09-2.47h-12.85l-.2,.06-.08,.19v30.72l.08,.2,.2,.08h7.22l.17-.08,.08-.2v-24.22h4.16c.44,0,.83,.15,1.19,.47l24.5,23.93,.18,.1h10.1c.12,0,.21-.05,.25-.16,.04-.1,.02-.2-.07-.28Zm30.51-30.73l-.2-.08h-44.22c-.09,0-.15,.02-.19,.08l-.06,.17v6.25l.06,.17c.04,.05,.1,.08,.19,.08h18.25v24.25l.06,.17c.04,.05,.1,.08,.19,.08h7.22l.18-.08,.07-.17v-24.25h18.25l.2-.08,.08-.17v-6.25l-.08-.17Zm33.86-.02l-.17-.06h-12.87c-2.3,0-4.32,.82-6.07,2.47l-28.84,28.34c-.08,.08-.1,.18-.06,.28,.04,.11,.12,.16,.25,.16h10.09l.19-.1,24.47-23.93c.35-.32,.76-.47,1.22-.47h4.15v24.22l.08,.2,.17,.08h7.22l.17-.08,.08-.2v-30.72l-.08-.19Z" />
        <path class="cls-1" d="M271.67,36.3v30.75l-.06,.17-.19,.08h-7.41l-.19-.1-24.5-23.93c-.35-.32-.75-.47-1.19-.47h-4.15v24.22l-.08,.2-.17,.08h-7.22l-.2-.08-.08-.2v-30.72l.08-.19,.2-.06h12.84c2.32,0,4.35,.82,6.1,2.47l18.5,18.18v-20.4l.06-.19,.19-.06h7.22l.19,.06,.06,.19Zm12.55-.19l-.19-.06h-7.22l-.18,.06-.07,.19v30.75l.07,.17,.18,.08h7.22l.19-.08,.06-.17v-30.75l-.06-.19Zm49.63,.02l-.17-.08h-35.88c-2.37,0-4.4,.83-6.09,2.48-1.69,1.66-2.53,3.65-2.53,5.99v22.53l.08,.17,.17,.08h7.25l.17-.08,.08-.17v-9.47h32.44l.2-.06,.08-.19v-6.25l-.08-.17-.2-.08h-32.44v-6.31c0-.48,.16-.89,.5-1.22,.33-.33,.74-.5,1.22-.5h35.03l.17-.06,.08-.19v-6.25l-.08-.17Zm57.11,.17v6.25l-.07,.17-.18,.08h-52.61l.54-1.19c.77-1.71,1.93-3.06,3.5-4.06,1.56-1,3.28-1.5,5.15-1.5h43.42l.18,.06,.07,.19Zm-8.39,24.5v6.25l-.07,.17-.18,.08h-35.03c-2.6,0-4.83-.91-6.69-2.74-1.85-1.82-2.78-4.01-2.78-6.57v-9.69h40.19l.19,.06,.06,.19v6.25l-.06,.17-.19,.08h-32.44v3.78c0,.48,.17,.88,.5,1.2,.34,.33,.74,.49,1.22,.49h35.03l.18,.08,.07,.2Zm-169.1-24.75c-.1,0-.18,.04-.22,.12l-5.16,10.59c-.75,1.29-1.78,1.94-3.09,1.94h-21.81v-12.41c0-.08-.03-.15-.08-.19-.05-.04-.12-.06-.2-.06h-7.22c-.06,0-.12,.02-.17,.06-.05,.04-.08,.1-.08,.19v30.72c0,.08,.03,.15,.08,.2,.05,.05,.11,.08,.17,.08h7.22c.08,0,.15-.03,.2-.08s.08-.12,.08-.2v-11.56h21.81c1.33,0,2.36,.65,3.09,1.94l4.75,9.75c.04,.1,.11,.16,.22,.16h8c.08,0,.15-.04,.2-.12,.05-.08,.06-.17,.02-.25l-5.78-11.97c-.52-1.06-1.2-2.02-2.03-2.88,.83-.85,1.51-1.81,2.03-2.88l6.19-12.81c.04-.08,.04-.16-.02-.23-.05-.07-.12-.11-.2-.11h-8Z" />
      </g>
    </g>
  </g>
</svg>'''


# Cyberpunk color scheme (HTML)
cyberpunk_styles_html = """
    body {
        font-family: 'Courier New', monospace;
        max-width: 900px;
        margin: 40px auto;
        padding: 20px;
        background-color: #0a0a0a;
    }
    .invoice {
        background: #1a1a1a;
        padding: 40px;
    }
    h1 {
        color: #00ffff;
        margin-bottom: 10px;
        font-size: 28px;
        text-shadow: 0 0 10px #00ffff;
    }
    .date {
        color: #00cccc;
        margin-bottom: 30px;
        font-size: 14px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th {
        background-color: #0d0d0d;
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #00ffff;
        font-weight: 600;
        color: #00ffff;
        font-size: 13px;
        text-transform: uppercase;
    }
    td {
        padding: 12px;
        border-bottom: 1px solid #333;
        color: #00cccc;
    }
    tr:hover {
        background-color: #252525;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.1);
    }
    .duration {
        text-align: right;
        font-weight: 500;
        color: #00ffff;
    }
    .total-row {
        font-weight: bold;
        background-color: #0d0d0d;
    }
    .total-row td {
        border-top: 2px solid #00ffff;
        border-bottom: 2px solid #00ffff;
        padding: 15px 12px;
        color: #00ffff;
    }
    .annotation {
        max-width: 400px;
    }
    .logo {
        margin-bottom: 20px;
        text-align: center;
    }
"""



# Printer-friendly color scheme (PDF)
printer_styles_pdf = """
    body {
        font-family: 'Courier New', monospace;
        margin: 0;
        padding: 0;
        background-color: white;
    }
    .invoice {
        background: white;
        padding: 0;
    }
    h1 {
        color: #008b8b;
        margin-bottom: 10px;
        font-size: 28px;
        border-bottom: 3px solid #00aaaa;
        padding-bottom: 10px;
    }
    .date {
        color: #555;
        margin-bottom: 30px;
        font-size: 14px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th {
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #008b8b;
        font-weight: 600;
        color: #008b8b;
        font-size: 13px;
        text-transform: uppercase;
    }
    td {
        padding: 12px;
        border-bottom: 1px solid #ddd;
        color: #333;
    }
    .duration {
        text-align: right;
        font-weight: 500;
        color: #008b8b;
    }
    .total-row {
        font-weight: bold;
    }
    .total-row td {
        padding-top: 30px;
        border-top: 3px solid #008b8b;
        border-bottom: 2px solid #008b8b;
        padding-bottom: 15px;
        color: #008b8b;
    }
    .annotation {
        max-width: 400px;
    }
    .logo {
        margin-bottom: 20px;
        background-color: #3a3a3a;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
"""

# Add @page rule for PDF format
page_rule = """
    @page {
        size: letter;
        margin: 1in;
    }
"""

# Select styles based on format
if args.format == 'html':
    # HTML uses cyberpunk style with box
    styles = cyberpunk_styles_html
    styles += """
    .invoice {
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        border: 1px solid #00ffff;
    }
"""
else:  # PDF format
    # PDF uses printer-friendly style
    styles = page_rule + printer_styles_pdf

# Build the HTML content
total_duration = 0
table_rows = ""

for interval in intervals:
    start = datetime.fromisoformat(interval["start"].replace("Z", "+00:00"))
    start_date = start.strftime("%Y-%m-%d")
    start_time = start.strftime("%H:%M")

    end_str = interval.get("end")
    if end_str:
        end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        end_date = end.strftime("%Y-%m-%d")
        end_time = end.strftime("%H:%M")

        # If the interval spans multiple days, show date range
        if start_date != end_date:
            date_str = f"{start_date} - {end_date}"
            time_range = f"{start_time} - {end_time}"
        else:
            date_str = start_date
            time_range = f"{start_time} - {end_time}"

        duration_seconds = (end - start).total_seconds()
        total_duration += duration_seconds
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        duration_str = f"{hours}h {minutes}m"
    else:
        date_str = start_date
        time_range = f"{start_time} - Open"
        duration_str = "Open"

    annotation = interval.get("annotation", "")

    table_rows += f"""            <tr>
                <td>{date_str}</td>
                <td>{time_range}</td>
                <td class="annotation">{annotation}</td>
                <td class="duration">{duration_str}</td>
            </tr>
"""

total_hours = int(total_duration // 3600)
total_minutes = int((total_duration % 3600) // 60)

html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
{styles}
    </style>
</head>
<body>
    <div class="invoice">
        <div class="logo">{logo_svg_cyberpunk}</div>
        <h1>Time Report</h1>
        <div class="date">Generated: {datetime.now().strftime("%B %d, %Y")}</div>
        <table>
            <tr>
                <th>Date</th>
                <th>Time</th>
                <th class="annotation">Description</th>
                <th>Duration</th>
            </tr>
{table_rows}            <tr class="total-row">
                <td colspan="3">Total</td>
                <td class="duration">{total_hours}h {total_minutes}m</td>
            </tr>
        </table>
    </div>
</body>
</html>"""

# If PDF format requested, convert HTML to PDF
if args.format == 'pdf':
    try:
        import subprocess
        import tempfile
        import os

        # Write HTML to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_output)
            temp_html = f.name

        # Convert to PDF using wkhtmltopdf or weasyprint
        if subprocess.run(['which', 'wkhtmltopdf'], capture_output=True).returncode == 0:
            subprocess.run(['wkhtmltopdf', temp_html, '-'], check=True)
        else:
            try:
                from weasyprint import HTML
                HTML(temp_html).write_pdf(sys.stdout.buffer)
            except ImportError:
                print("Error: PDF generation requires either 'wkhtmltopdf' or 'weasyprint' to be installed.", file=sys.stderr)
                print("Install with: brew install wkhtmltopdf  OR  pip install weasyprint", file=sys.stderr)
                sys.exit(1)

        os.unlink(temp_html)

    except Exception as e:
        print(f"Error generating PDF: {e}", file=sys.stderr)
        sys.exit(1)
else:
    # Output HTML
    print(html_output)   
