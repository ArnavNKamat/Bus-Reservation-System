from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "web" / "templates" / "index.html"
STATIC = ROOT / "web" / "static"
OUTPUT = ROOT / "site"


def main():
    html = TEMPLATE.read_text(encoding="utf-8")
    css_template_ref = "{{ url_for('static', filename='css/style.css') }}"
    js_template_ref = "{{ url_for('static', filename='js/app.js') }}"

    if html.count(css_template_ref) != 1 or html.count(js_template_ref) != 1:
        raise RuntimeError("Expected exactly one Flask CSS and JavaScript asset reference.")

    html = html.replace(css_template_ref, "static/css/style.css")
    html = html.replace(
        js_template_ref,
        'static/js/demo-api.js"></script>\n    <script src="static/js/app.js',
    )
    html = html.replace("🌴 Official Goa Travel Portal", "🌴 Interactive Portfolio Demo")
    html = html.replace("Instant E-Tickets", "Sample E-Tickets")
    html = html.replace(
        "Secure UPI, Card & Net Banking payments",
        "Simulated checkout · No real payments",
    )
    html = html.replace("Passenger Details & Payment", "Passenger Details · Demo Checkout")
    html = html.replace("2. Payment Method", "2. Demo Payment Options (Not Processed)")
    html = html.replace("Pay & Confirm Booking", "Create Demo Booking")
    html = html.replace(
        '<main class="main-content">',
        '<main class="main-content">\n'
        '        <aside role="note" style="margin: 1rem auto; max-width: 1200px; padding: 0.85rem 1rem; border-radius: 12px; background: #fff7ed; color: #9a3412; text-align: center;">'
        '<strong>Portfolio demo:</strong> Sample schedules, sign-in, bookings, and payments are simulated in this demo. '
        'Do not enter real personal or payment information.</aside>',
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    (OUTPUT / ".nojekyll").touch()
    target_static = OUTPUT / "static"
    shutil.copytree(STATIC, target_static, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
