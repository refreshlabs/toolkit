from datetime import date

import click
from flask import current_app

from app.extensions import db
from app.models import LabStatus, TransparencyReport, Video
from app.services.youtube import YouTubeSyncError, sync_videos


def register_cli(app):
    @app.cli.command("sync-youtube")
    def sync_youtube():
        """Fetch videos from the configured YouTube channel and upsert them into the Video table."""
        api_key = current_app.config["YOUTUBE_API_KEY"]
        channel_id = current_app.config["YOUTUBE_CHANNEL_ID"]
        try:
            created, updated = sync_videos(api_key, channel_id)
        except YouTubeSyncError as e:
            raise click.ClickException(str(e))
        click.echo(f"YouTube sync complete: {created} created, {updated} updated.")

    @app.cli.command("seed-db")
    def seed_db():
        """Create tables and populate placeholder content for a fresh install."""
        db.create_all()

        if not Video.query.first():
            db.session.add_all(
                [
                    Video(
                        title="Coming Soon: What Is Bitcoin Mining?",
                        description="An introduction to proof-of-work and how mining secures the network.",
                        category="Bitcoin",
                        published_date=date.today(),
                        external_url=None,
                        thumbnail_url=None,
                        is_placeholder=True,
                    ),
                    Video(
                        title="Coming Soon: Inside the Living Laboratory",
                        description="A tour of the Refresh Labs mining demonstration setup.",
                        category="Mining",
                        published_date=date.today(),
                        external_url=None,
                        thumbnail_url=None,
                        is_placeholder=True,
                    ),
                    Video(
                        title="Coming Soon: Getting Started with Linux",
                        description="Your first steps into open-source operating systems.",
                        category="Open Source",
                        published_date=date.today(),
                        external_url=None,
                        thumbnail_url=None,
                        is_placeholder=True,
                    ),
                    Video(
                        title="Coming Soon: HAM Radio for Beginners",
                        description="Why amateur radio still matters in a connected world.",
                        category="HAM Radio",
                        published_date=date.today(),
                        external_url=None,
                        thumbnail_url=None,
                        is_placeholder=True,
                    ),
                ]
            )

        if not TransparencyReport.query.first():
            db.session.add(
                TransparencyReport(
                    period="2026",
                    donations_total_cents=0,
                    expense_website_cents=0,
                    expense_content_cents=0,
                    expense_irs_cents=0,
                    expense_lab_cents=0,
                    btc_purchased=0,
                    btc_mined=0,
                    hashpower_purchased="0",
                    resources_published=0,
                    events_hosted=0,
                )
            )

        if not LabStatus.query.first():
            db.session.add(
                LabStatus(
                    hashrate="Coming Soon",
                    mining_provider="Coming Soon",
                    mining_period="Coming Soon",
                    btc_produced="Coming Soon",
                    mining_costs="Coming Soon",
                    estimated_btc_value="Coming Soon",
                    educational_content_produced="Coming Soon",
                    status="Planning",
                )
            )

        db.session.commit()
        click.echo("Database seeded with placeholder content.")
