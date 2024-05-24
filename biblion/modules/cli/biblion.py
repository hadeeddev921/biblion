# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Click command-line utilities."""

import click

from biblion.modules.acquisition.cli import acquisition
from biblion.modules.api_harvester.cli import api_harvester
from biblion.modules.cli.messages import messages
from biblion.modules.entities.remote_entities.cli import entity
from biblion.modules.migrations.cli import migrations
from biblion.modules.monitoring.cli import monitoring
from biblion.modules.notifications.cli import notifications
from biblion.modules.stats.cli import stats
from biblion.schedulers import scheduler

from .documents import documents
from .fixtures import fixtures
from .index import index
from .utils import utils


@click.group()
def biblion():
    """Biblion management commands."""


biblion.add_command(acquisition)
biblion.add_command(api_harvester)
biblion.add_command(documents)
biblion.add_command(entity)
biblion.add_command(fixtures)
biblion.add_command(index)
biblion.add_command(migrations)
biblion.add_command(messages)
biblion.add_command(monitoring)
biblion.add_command(notifications)
biblion.add_command(scheduler)
biblion.add_command(stats)
biblion.add_command(utils)
