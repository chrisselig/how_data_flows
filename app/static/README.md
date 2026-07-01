# Corporate Theme Bundle

Shared branding for all HR course apps. **Self-contained and copyable** — no
Claude, no build step, no extra dependencies beyond Streamlit.

## What's in the bundle

| File | Purpose |
| --- | --- |
| `theme.css` | All styling. Brand palette lives in the `:root` block at the top. |
| `logo.svg` | **Placeholder** company logo (top-right of the header). |
| `background.svg` | **Placeholder** full-app background image. |
| `../theme.py` | Loader — injects the CSS and renders the header. |
| `../../.streamlit/config.toml` | Forces Streamlit to the light base theme. |

## Reuse in another course

1. Copy `app/theme.py`, the whole `app/static/` folder, and
   `.streamlit/config.toml` into the other course.
2. After `st.set_page_config(...)`, call:
   ```python
   from app.theme import apply_theme
   apply_theme(default_name="That Course Title")
   ```
   That's the only code change.

## Swapping the placeholders (in the corporate environment)

- **Logo** — drop a real `logo.png` (or `.jpg` / `.svg`) into this folder. Real
  files are picked up ahead of the placeholder automatically.
- **Background** — drop a real `background.png` (or `.jpg` / `.svg`) here.
- **App / report name** — set the `APP_NAME` environment variable per
  deployment; it overrides the `default_name` passed in code and is shown in
  orange on the left of the header.

## Colours — plug in the corporate palette

Every colour is a CSS variable in the `:root` block of `theme.css`. To apply
the official corporate palette (e.g. the values from the corporate branding
GitHub Copilot skill), edit only those variables — nothing else references raw
hex codes:

```css
:root {
    --brand-orange:  #E8730C;   /* app/report name + header bar */
    --brand-primary: #1B4F72;   /* headings / KPI values */
    --brand-accent:  #2980B9;   /* secondary accents */
    /* ... */
}
```

Also update `primaryColor` in `.streamlit/config.toml` to match `--brand-orange`
so Streamlit's own controls (buttons, sliders) stay on-brand.

> Note: the PDF certificate (`src/certificate.py`) uses its own colour
> constants — it renders via reportlab, not CSS, so those are separate.
