"""

"""
import pathlib
import contextlib

import transaction
from clldutils import db
from clldutils import clilib
from clld.scripts.util import SessionContext, ExistingConfig, get_env_and_settings
from pyacc import ACC

import acc
from acc.scripts.initializedb import main, prime_cache

PROJECT_DIR = pathlib.Path(acc.__file__).parent.parent


def register(parser):
    parser.add_argument(
        "--config-uri",
        action=ExistingConfig,
        help="ini file providing app config",
        default=str(PROJECT_DIR / 'development.ini'))
    parser.add_argument(
        '--doi',
        default=None,
    )
    parser.add_argument(
        '--prime-cache-only',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--repos',
        default=pathlib.Path(PROJECT_DIR.parent / 'acc-data'),
        help='Clone of acc-data',
        type=clilib.PathType,
    )


def run(args):
    args.env, settings = get_env_and_settings(args.config_uri)

    with contextlib.ExitStack() as stack:
        stack.enter_context(db.FreshDB.from_settings(settings, log=args.log))
        stack.enter_context(SessionContext(settings))
        args.api = ACC(args.repos)
        if not args.prime_cache_only:
            with transaction.manager:
                main(args)
        with transaction.manager:
            prime_cache(args)
