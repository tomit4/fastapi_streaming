<div align="center">
    <img
    style="scale: 0.7; margin-bottom: -3em;"
    src="https://raw.githubusercontent.com/tomit4/fastapi_app/main/src/fastapi_app/public/fastapi-logo.webp">
<h1 style="border: none">FastAPI App</h1>
</div>

<h2 style="border: none">Introduction</h2>

This repository contains a bare bones starter template for a backend using
[FastAPI](https://fastapi.tiangolo.com/)

**PreRequisite Dependencies:**

To use this as a basic template for future projects, you'll first need to have
[git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git),
[python](https://www.python.org/downloads/),
[docker](https://docs.docker.com/engine/install/), and
[rye](https://rye.astral.sh/guide/installation/) installed.

You'll also probably want to have a basic familiarity with the command line
(examples here are in
[bash](https://www.gnu.org/software/bash/manual/bash.html)).

**Getting Started:**

Once those are installed, you can clone this repository in a directory of your
choosing:

```sh
git clone https://github.com/tomit4/fastapi_app &&\
cd fastapi_app
```

You'll also need to simply copy the included `env-sample` file as a `.env` to
adjust from the default `HOST` and `PORT`:

```sh
cp env-sample .env
```

Once cloned and inside the project's directory. go ahead and use rye to initiate
the virtual environment (defaults to a `.venv` directory):

```sh
rye sync
```

This will also install all necessary dependencies needed. After that, you'll
need to instantiate your virtual environment like so:

```sh
source .venv/bin/activate
```

You'll need to migrate the database so that the essential tables are
established. You can do this with a custom `rye` script that uses `alembic`
under the hood:

```sh
rye run upgrade head
```

After you've migrated the database, you can then run the server itself using the
`dev` script:

```sh
rye run dev
```

The default port utilized for this template is 8000. So once you see the
fastapi-cli's output, indicating successful startup of the server, you can
simply navigate in your browser to localhost:8000/docs to see the OpenAPI
documentation of the app.

### About The App

This App is just a template, but can be utilized as a model on how to organize
future applications/projects.

**The Rye Package Manager**

This project utilizes the modern python project/package manager
[Rye](https://rye.astral.sh/). Please see their
[Installation Instructions](https://rye.astral.sh/guide/installation/) if you
don't have it installed.

While the official [User Guide](https://rye.astral.sh/guide/) should provide you
with all the information you'll need to get started using Rye, Here are a few
common commands you might find yourself needing to use throughout building your
application

```sh
# Adding a package
rye add package_name
# Removing a package
rye remove package_name
# Adding a dev dependency
rye add --dev package_name
# Removing a dev dependency
rye remove --dev package_name
# Syncing Your Project With The Virtual Environment
# (run after installing/uninstalling dependencies)
rye sync
```

Should you find yourself ready to build/publish your application, please consult
Rye's Official Documentation on
[Building and Publishing](https://rye.astral.sh/guide/publish/).

**SQLAlchemy And Setting Up The Database**

This App template uses the [SQLAlchemy ORM](https://www.sqlalchemy.org/), and
thusly can utilize any of the classic SQL databases including [SQLite](),
[Postgresql](https://www.postgresql.org/), [MySQL](https://www.mysql.com/) &
[MariaDB](https://mariadb.org/),
[Oracle](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Introduction-to-Oracle-SQL.html),
and [MS-SQL](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

**A Note on AsyncIO**:

This App template sets up SQLAlchemy to work with PostgreSQL
<em>asynchronously</em>. The configuration is based off of
[This Handy Tutorial](https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308)
as well as
[This Article](https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html).

You can also further read more about async usage in SQLAlchemy
[here](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).

**Instantiating PostgreSQL Via Docker**

This version of the App template gives you the option of utilizing either SQLite
or PostgreSQL databases (and uses an in memory SQLite DB in testing). Depending
on which DB you want to use, you'll need to adjust a few settings. By default,
the App uses a PostgreSQL database within a [Docker](https://www.docker.com/)
container (setup using [docker compose](https://docs.docker.com/compose/)).

To initialize the database, you simply have to fill out the appropriate Database
URI fields within your `.env` file:

```
# Postgres Config
PG_HOST="127.0.0.1"
PG_PORT=5936
DB_PORT=5432
PG_USER="admin"
PG_DB="app_db"
PG_CONTAINER_NAME="app_db"
PG_PASS="postgres"
```

If you are just working in development and have port 5936 available on your
development machine, you can leave these fields the same (but I advise that
should you push your application to production that you adjust these default
settings).

Once your `.env` variables are set up, you can use `docker compose` to
instantiate your docker images/containers:

```sh
docker compose -f ./docker-compose.yml up -d
```

You can check the status of your docker containers to ensure they are running
like so:

```sh
docker container ls -a
```

Once you are sure your docker containers are running you can then use
[Alembic](https://alembic.sqlalchemy.org/en/latest/) to migrate your initial
tables into the database.

**Using Alembic To Set Up Your Initial Tables**

You can initialize your first database migration by utilizing a prepared
`upgrade` script (if you want to see how they work, take a look at the
[pyproject.toml](./pyproject.toml) file):

```sh
rye run upgrade head
```

Or you can invoke `alembic` directly like so:

```sh
alembic --config ./src/fastapi_app/alembic.ini upgrade head
```

Should you need to downgrade the migration (roll back your previous changes to
the database), you can use a similar `downgrade` script:

```sh
rye run downgrade -1
```

Or you can invoke `alembic` directly like so:

```sh
alembic --config ./src/fastapi_app/alembic.ini downgrade -1
```

Which will downgrade alembic by exactly 1 migration (you can further revert back
your changes to the database by repeatedly invoking this script, or invoking
`alembic` directly as shown above and simply adjust the negative number at the
end).

You can find all migration scripts within the `src/fastapi_app/migrations`
directory. Should you need to add new tables you can generate a new migration
script:

```sh
rye run generate "Added users table"
```

Or you can invoke it directly like so:

```sh
alembic --config ./src/fastapi_app/alembic.ini revision --autogenerate -m "Added users table"
```

**Static Files**

FastAPI provides for use of static files very easily. To serve static files,
place them in the `src/fastapi_app/public` folder. The server is set up to serve
any static files placed here by default. To view them in your browser, simply
enter the url
<em>localhost:8000/public/<b>name_of_your_file.jpg</b></em> and you should see
your file displayed there.

Provided with this template is a sample webp of the FastAPI Logo you can view
from your browser while the server is running. Simply visit
<em>localhost:8000/public/fastapi-logo.webp</em>

Should you wish to know more about static files in FastAPI, please see their
[tutorial on the subject](https://fastapi.tiangolo.com/tutorial/static-files/).

**Testing**

FastAPI favors using [pytest](https://docs.pytest.org/en/stable/) to run unit
tests for FastAPI applicactions. If you wish to run the tests, don't utilize
`pytest` directly. Instead, simply invoke `rye test` to run them (uses `pytest`
under the hood, do <em>not</em> invoke `pytest` directly as that will error out
when trying to import dependencies):

```sh
rye test
```

**Editor Tooling**

This project utilizes some additional editor tooling for use with python. These
include:

- [black (code formatter)](https://black.readthedocs.io/en/stable/index.html)
- [isort (dependency organizer)](https://pycqa.github.io/isort/)
- [pyright (python linter)](https://github.com/microsoft/pyright)

You can install the [VSCode](https://code.visualstudio.com/) extensions via your
editor or you can download them directly from the
[Visual Studio Marketplace](https://marketplace.visualstudio.com/):

- [VSCode black](https://marketplace.visualstudio.com/items?itemName=mikoz.black-py)
- [VSCode isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
- [VSCode pyright](https://marketplace.visualstudio.com/items?itemName=ms-pyright.pyright)

Additionally, the Neovim equivalents can be downloaded directly, downloaded
using a extensions tool like
[Mason](https://github.com/williamboman/mason.nvim):

- [NeoVim black](https://github.com/averms/black-nvim)
- [NeoVim isort](https://github.com/stsewd/isort.nvim)
- [NeoVim pyright](https://www.andersevenrud.net/neovim.github.io/lsp/configurations/pyright/)

I personally use [NeoVim](https://neovim.io/) and an all in one formatter,
[conform](https://github.com/stevearc/conform.nvim). I did, however, download
pyright using Mason.

<h2 style="border: none;">Conclusion</h2>

This is the most organized workflow I've found using FastAPI (or any Python
project for that matter). There are more features I plan on adding to this
template like working with
[OAuth2 and JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
This repository is mainly meant for my own personal use for scaffolding off of
into future projects, but perhaps you, dear reader, might also find it useful.
