# Terminal window

The profile header is one GitHub code block (`<pre>`) that acts as a macOS-style terminal window. Its contents are transparent SVGs drawn on the code block's own background, so the window follows GitHub's light and dark themes.

Session shown, top to bottom:

| Step | Content | Source |
| --- | --- | --- |
| Title bar | Close, minimise and zoom lights (red, yellow, green) and the window title | `terminal-top*.svg` |
| `whoami` | Block-pixel name and full name | `terminal-top*.svg` |
| `cat about.txt` | Role lines | `terminal-top*.svg` |
| `ls links/` | Seven separate clickable anchors, one SVG each | `terminal-link-*.svg` |
| `fastfetch` | Arch logo, key/value rows, colour swatches, idle prompt with blinking cursor | `terminal-fetch*.svg` |
| Status line | tmux-style segment plus live views, followers and stars badges | `terminal-status.svg`, Komarev, Shields |

Metrics, top languages, streak, snake and the toolbox footer stay below the window and are unchanged.

## Variants

Each asset has a desktop version (800 px wide) and a `-compact` version (340 px wide). README.md switches at `max-width: 1000px` with a `<picture><source>` element. The toolbox footer keeps its own 600 px breakpoint.

## Editing

Run `python3 scripts/build_terminal_art.py` to regenerate every file in `Assets/terminal/`. All text, colours and timings are constants at the top of that script:

| Change | Edit |
| --- | --- |
| Role lines | `ABOUT` |
| fastfetch rows | `FIELDS` |
| Prompt | `PROMPT` |
| Links | `LINKS` (and the matching anchors in README.md) |
| Colours | `PALETTE` (dark, light) and `LETTER_COLORS` |
| Window title | `Layout.title` in `DESKTOP` and `COMPACT` |

Alt text in README.md is separate from the text drawn inside the SVGs; change both. The Arch logo path is read from `Assets/profile/toolbox-logos.json`.

Run `python3 scripts/preview_profile.py` for a local preview. The external badges need internet access.

## Behaviour

The typing, reveal and cursor effects are CSS animations that run once on load. Without animation support, or with `prefers-reduced-motion`, the final state is shown immediately. The only looping animation is the blinking cursor on the last prompt, which is disabled under reduced motion. Text uses `textLength`, so column alignment does not depend on the viewer's monospace font.

The palette is Catppuccin Mocha (dark) and Latte (light). Traffic-light colours are the macOS ones and do not change with the theme.
