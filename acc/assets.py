from pathlib import Path

from clld.web.assets import environment

import acc


environment.append_path(
    Path(acc.__file__).parent.joinpath('static').as_posix(),
    url='/acc:static/')
environment.load_path = list(reversed(environment.load_path))
