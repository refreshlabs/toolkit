# Refresh Labs

Refresh Labs is a 501(c)(3) educational nonprofit exploring open systems -
Bitcoin, proof-of-work, open-source software, digital literacy,
communications technology, and related fields - through educational media,
hands-on demonstrations, transparent experimentation, and community
programs.

The organization operates a **Living Laboratory**: a small Bitcoin mining
operation run purely as an educational demonstration, not as a
profit-seeking activity. Its purpose is to teach how decentralized
networks, proof-of-work, and mining economics actually work, using real
operational data - published transparently, costs and losses included.

This repository is the organization's public website and is developed in
the open so others can learn from, reproduce, and improve it.

## Principles

- **Education first.** Every feature serves the mission of teaching.
- **Transparency always.** Donations, expenses, and mining activity are
  published as an annual public report.
- **Open source.** The code and, wherever practical, the content are public.
- **Simple to maintain.** This is run by a small volunteer nonprofit, not an
  engineering team - the stack stays boring on purpose.

## Tech Stack

- **Backend:** Flask (Python), application-factory pattern
- **Templates:** Jinja2
- **Database:** SQLite via Flask-SQLAlchemy (videos, events, transparency
  reports, Living Laboratory status)
- **Content:** Tutorials are Markdown files with frontmatter, rendered at
  request time - no database needed to publish a tutorial
- **Styling:** Tailwind CSS (Play CDN - no build step required for v1)

No user accounts, membership system, payment processing, or CMS. Content is
edited by editing files in this repository and redeploying.

## Project Structure

```
app/
  __init__.py        application factory
  extensions.py       shared Flask extensions (db)
  cli.py              `flask seed-db` command
  models/              Video, Event, TransparencyReport, LabStatus
  routes/              blueprints: main, learn, laboratory, events
  services/            tutorials.py - Markdown content loader
  templates/           Jinja2 templates
  static/              CSS/images
  content/
    tutorials/          Markdown tutorial files
config.py              app configuration
run.py                 local dev entrypoint
requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=run.py
flask seed-db      # creates instance/refreshlabs.db and placeholder content

python run.py       # http://127.0.0.1:5000
```

## Adding Content

- **Tutorials:** add a new `.md` file to `app/content/tutorials/` with
  frontmatter (`title`, `description`, `category`, `date`). No code change
  or database migration needed.
- **Videos / Events / Transparency reports:** currently added via the
  database (`flask shell` or a small script using the models in
  `app/models/`). A lightweight import script may be added later.

## Development Roadmap

- [ ] Connect the Living Laboratory dashboard to a real mining pool API,
      Bitcoin node, and power monitoring hardware
- [ ] Publish the first real transparency report
- [ ] Add real video content and thumbnails
- [ ] Expand tutorials: Lightning Network, Linux, HAM radio, networking labs,
      renewable energy demonstrations
- [ ] School / community educational partnerships
- [ ] Wire up real donation processing
- [ ] Replace Tailwind Play CDN with a compiled build once the design
      stabilizes

## Open Source Philosophy

Refresh Labs believes understanding is built by seeing how things actually
work - including the parts that don't work yet. This codebase, like the
Living Laboratory itself, is published so anyone can study it, question it,
and build on it.
