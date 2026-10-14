# ASCII art shortlist

The three installed scene assets come from [ascii.rest](https://ascii.rest/), with the generator's MIT license preserved in `assets/js/vendor/LICENSE.ascii.txt`:

- [Cloud Sea](https://ascii.rest/cloud-sea/) — the homepage's warm sunset above drifting clouds.
- [Night Coast](https://ascii.rest/night-coast/) — the journal's blue night scene with a lighthouse and moving beam.
- [Edge Orbit](https://ascii.rest/edge-orbit/) — the projects archive's view of Earth's night side and network arcs.

## Selected small animations

The small ascii.rest pieces from the earlier shortlist were not used. Birds and Squirrel come from the [ASCII Motion community](https://ascii-motion.app/community); the world map uses public-domain Natural Earth land polygons:

| Piece | Placement and behavior | Preview and source |
| --- | --- | --- |
| Birds by CameronFoxly | Homepage footer; takes off on arrival, leaves completely, then stays hidden across page visits until a full reload | [See Birds](https://ascii-motion.app/community/project/d0a249d8-acf0-4e81-939b-18053b5cdc3e) |
| World map | Shimmering coastline character grid below the homepage projects; runs once and settles | [Natural Earth](https://www.naturalearthdata.com/) |
| Squirrel by CameronFoxly | Small illustration near the end of the Yarplus case study; runs once | [See Squirrel](https://ascii-motion.app/community/project/5097d8dd-9b38-4786-b7dd-dcb18754584d) |

These placements are deliberately fixed rather than random on every page load. They preserve the reading flow and avoid repeating the same decorations throughout the site. Assets are compact local character grids with no external runtime requests; the birds retain a locally hosted 26 KB VGA font. Full artist credits, permission details, and adaptation notes are in [assets/art/CREDITS.md](assets/art/CREDITS.md). The earlier Crosshatch Noise asset has been removed.

The compact Telegram icon is converted from the [official Telegram SVG](https://telegram.org/img/t_logo.svg) into a 28×16 character grid, also saved as `assets/art/telegram.txt`. It appears once on the homepage's contact action and once in each other page's footer. Telegram permits this kind of logo use on [its press page](https://telegram.org/press#telegram-logos).

## More sources

- [ASCII Motion community](https://ascii-motion.app/community) — the user's preferred gallery of animations and remixable projects.
- [ASCII Motion editor](https://ascii-motion.app/) — author or adjust a character animation and export it for a static site.
- [ASCII Art Archive animations](https://www.asciiart.eu/animations) — browser previews of effects, spinning shapes, ripples, and other text animations.
- [ASCII Art Archive cats](https://www.asciiart.eu/animals/cats) — a static character collection when a quiet, non-animated detail is preferable.
