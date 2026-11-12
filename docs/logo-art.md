# Full-color logo footer

The footer uses the original vector shapes and full colors for Claude, GitLab, Git, Arch Linux and Linux/Tux. Codex and GitHub use their monochrome marks: white on dark themes and black on light themes. There is no global green recoloring, logo dimming, moving wash, or grayscale filter. All marks remain at full opacity.

A seven-second three-pixel float and a small travelling underline supply the motion. Labels stay visible. The phone layout uses two rows. Reduced-motion preferences disable both effects. There is no new workflow, secret, JavaScript, external font or runtime image request.

## Edit and regenerate

Run `python3 scripts/build_logo_art.py` to regenerate the two footer SVGs. All source artwork is bundled in `Assets/profile/toolbox-logos.json`. The generator preserves source colors, gradients, transforms and viewBoxes, and prefixes gradient IDs so marks cannot interfere with each other.

Run `python3 scripts/preview_profile.py` to preview the whole README locally. Refresh after edits; Ctrl+C stops the server. For a still frame, use `python3 scripts/build_logo_art.py --frame 4 --output /tmp/toolbox-preview`.

## Vector sources

| Mark | Source |
| --- | --- |
| Claude | https://github.com/lobehub/lobe-icons/blob/master/packages/static-svg/icons/claude-color.svg |
| Codex | https://github.com/lobehub/lobe-icons/blob/master/packages/static-svg/icons/codex.svg |
| GitHub | https://github.com/lobehub/lobe-icons/blob/master/packages/static-svg/icons/github.svg |
| GitLab | https://github.com/devicons/devicon/blob/master/icons/gitlab/gitlab-original.svg |
| Git | https://github.com/devicons/devicon/blob/master/icons/git/git-original.svg |
| Arch Linux | https://github.com/devicons/devicon/blob/master/icons/archlinux/archlinux-original.svg |
| Linux/Tux | https://github.com/devicons/devicon/blob/master/icons/linux/linux-original.svg |

The complete MIT notices for Lobe Icons and Devicon are included in `docs/licenses/`. Brand names and marks belong to their owners; this personal artwork does not imply affiliation or endorsement.
