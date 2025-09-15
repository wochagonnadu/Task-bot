dev/ARCHIVE/Task-bot on  master [✘✏️ ?] via 🐍  ❯ docker-compose logs -f
taskbot_db  |
taskbot_db  | PostgreSQL Database directory appears to contain a database; Skipping initialization
taskbot_db  |
taskbot_db  | 2025-09-15 09:10:44.416 UTC [1] LOG:  starting PostgreSQL 13.22 (Debian 13.22-1.pgdg13+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
taskbot_db  | 2025-09-15 09:10:44.417 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
taskbot_db  | 2025-09-15 09:10:44.417 UTC [1] LOG:  listening on IPv6 address "::", port 5432
taskbot_db  | 2025-09-15 09:10:44.419 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
taskbot_db  | 2025-09-15 09:10:44.421 UTC [26] LOG:  database system was shut down at 2025-09-15 09:10:30 UTC
taskbot_db  | 2025-09-15 09:10:44.426 UTC [1] LOG:  database system is ready to accept connections
taskbot_app  | 🔄 Ждём доступности базы данных...
taskbot_app  | 🔄 Ожидание доступности базы данных: db:5432...
taskbot_app  | Connection to db (172.19.0.2) 5432 port [tcp/postgresql] succeeded!
taskbot_app  | ✅ БД доступна!
taskbot_app  | ▶️ Запуск приложения...
taskbot_app  | ✅ WORK_START_TIME: 09:30
taskbot_app  | ✅ WORK_END_TIME: 17:30
taskbot_app  | 2025-09-15 12:10:50,608 - __main__ - INFO - Запуск BotRunner...
taskbot_app  | 2025-09-15 12:10:50,608 - __main__ - INFO - Инициализация базы данных...
taskbot_app  | 2025-09-15 12:10:51,818 - src.database.db - ERROR - Неожиданная ошибка при инициализации БД:
taskbot_app  | Traceback (most recent call last):
taskbot_app  |   File "/app/src/database/db.py", line 49, in init_db
taskbot_app  |     async with engine.begin() as conn:
taskbot_app  |   File "/usr/local/lib/python3.11/contextlib.py", line 210, in __aenter__
taskbot_app  |     return await anext(self.gen)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 1064, in begin
taskbot_app  |     async with conn:
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/base.py", line 121, in __aenter__
taskbot_app  |     return await self.start(is_ctxmanager=True)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 274, in start
taskbot_app  |     await greenlet_spawn(self.sync_engine.connect)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
taskbot_app  |     result = context.throw(*sys.exc_info())
taskbot_app  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3274, in connect
taskbot_app  |     return self._connection_cls(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 146, in __init__
taskbot_app  |     self._dbapi_connection = engine.raw_connection()
taskbot_app  |                              ^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3298, in raw_connection
taskbot_app  |     return self.pool.connect()
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 449, in connect
taskbot_app  |     return _ConnectionFairy._checkout(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1263, in _checkout
taskbot_app  |     fairy = _ConnectionRecord.checkout(pool)
taskbot_app  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
taskbot_app  |     rec = pool._do_get()
taskbot_app  |           ^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 179, in _do_get
taskbot_app  |     with util.safe_reraise():
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
taskbot_app  |     raise exc_value.with_traceback(exc_tb)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
taskbot_app  |     return self._create_connection()
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 390, in _create_connection
taskbot_app  |     return _ConnectionRecord(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 674, in __init__
taskbot_app  |     self.__connect()
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 900, in __connect
taskbot_app  |     with util.safe_reraise():
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
taskbot_app  |     raise exc_value.with_traceback(exc_tb)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 896, in __connect
taskbot_app  |     self.dbapi_connection = connection = pool._invoke_creator(self)
taskbot_app  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 646, in connect
taskbot_app  |     return dialect.connect(*cargs, **cparams)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 622, in connect
taskbot_app  |     return self.loaded_dbapi.connect(*cargs, **cparams)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 961, in connect
taskbot_app  |     await_only(creator_fn(*arg, **kw)),
taskbot_app  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
taskbot_app  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
taskbot_app  |     value = await result
taskbot_app  |             ^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connection.py", line 2421, in connect
taskbot_app  |     return await connect_utils._connect(
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1075, in _connect
taskbot_app  |     raise last_error or exceptions.TargetServerAttributeNotMatched(
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1049, in _connect
taskbot_app  |     conn = await _connect_addr(
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 886, in _connect_addr
taskbot_app  |     return await __connect_addr(params, True, *args)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 931, in __connect_addr
taskbot_app  |     tr, pr = await connector
taskbot_app  |              ^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 818, in _create_ssl_connection
taskbot_app  |     new_tr = await loop.start_tls(
taskbot_app  |              ^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/asyncio/base_events.py", line 1268, in start_tls
taskbot_app  |     await waiter
taskbot_app  |   File "/usr/local/lib/python3.11/asyncio/sslproto.py", line 578, in _on_handshake_complete
taskbot_app  |     raise handshake_exc
taskbot_app  | ConnectionResetError
taskbot_app  | 2025-09-15 12:10:51,831 - __main__ - ERROR - Критическая ошибка:
taskbot_app  | Traceback (most recent call last):
taskbot_app  |   File "/app/src/main.py", line 84, in init_bots
taskbot_app  |     await init_db()
taskbot_app  |   File "/app/src/database/db.py", line 49, in init_db
taskbot_app  |     async with engine.begin() as conn:
taskbot_app  |   File "/usr/local/lib/python3.11/contextlib.py", line 210, in __aenter__
taskbot_app  |     return await anext(self.gen)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 1064, in begin
taskbot_app  |     async with conn:
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/base.py", line 121, in __aenter__
taskbot_app  |     return await self.start(is_ctxmanager=True)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 274, in start
taskbot_app  |     await greenlet_spawn(self.sync_engine.connect)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
taskbot_app  |     result = context.throw(*sys.exc_info())
taskbot_app  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3274, in connect
taskbot_app  |     return self._connection_cls(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 146, in __init__
taskbot_app  |     self._dbapi_connection = engine.raw_connection()
taskbot_app  |                              ^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3298, in raw_connection
taskbot_app  |     return self.pool.connect()
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 449, in connect
taskbot_app  |     return _ConnectionFairy._checkout(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1263, in _checkout
taskbot_app  |     fairy = _ConnectionRecord.checkout(pool)
taskbot_app  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
taskbot_app  |     rec = pool._do_get()
taskbot_app  |           ^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 179, in _do_get
taskbot_app  |     with util.safe_reraise():
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
taskbot_app  |     raise exc_value.with_traceback(exc_tb)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
taskbot_app  |     return self._create_connection()
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 390, in _create_connection
taskbot_app  |     return _ConnectionRecord(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 674, in __init__
taskbot_app  |     self.__connect()
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 900, in __connect
taskbot_app  |     with util.safe_reraise():
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
taskbot_app  |     raise exc_value.with_traceback(exc_tb)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 896, in __connect
taskbot_app  |     self.dbapi_connection = connection = pool._invoke_creator(self)
taskbot_app  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 646, in connect
taskbot_app  |     return dialect.connect(*cargs, **cparams)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 622, in connect
taskbot_app  |     return self.loaded_dbapi.connect(*cargs, **cparams)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 961, in connect
taskbot_app  |     await_only(creator_fn(*arg, **kw)),
taskbot_app  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
taskbot_app  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
taskbot_app  |     value = await result
taskbot_app  |             ^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connection.py", line 2421, in connect
taskbot_app  |     return await connect_utils._connect(
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1075, in _connect
taskbot_app  |     raise last_error or exceptions.TargetServerAttributeNotMatched(
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1049, in _connect
taskbot_app  |     conn = await _connect_addr(
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 886, in _connect_addr
taskbot_app  |     return await __connect_addr(params, True, *args)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 931, in __connect_addr
taskbot_app  |     tr, pr = await connector
taskbot_app  |              ^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 818, in _create_ssl_connection
taskbot_app  |     new_tr = await loop.start_tls(
taskbot_app  |              ^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/asyncio/base_events.py", line 1268, in start_tls
taskbot_app  |     await waiter
taskbot_app  |   File "/usr/local/lib/python3.11/asyncio/sslproto.py", line 578, in _on_handshake_complete
taskbot_app  |     raise handshake_exc
taskbot_app  | ConnectionResetError
taskbot_app  | 2025-09-15 12:10:51,833 - __main__ - ERROR - Неожиданная ошибка:
taskbot_app  | Traceback (most recent call last):
taskbot_app  |   File "/app/src/main.py", line 174, in run
taskbot_app  |     await self.init_bots()
taskbot_app  |   File "/app/src/main.py", line 84, in init_bots
taskbot_app  |     await init_db()
taskbot_app  |   File "/app/src/database/db.py", line 49, in init_db
taskbot_app  |     async with engine.begin() as conn:
taskbot_app  |   File "/usr/local/lib/python3.11/contextlib.py", line 210, in __aenter__
taskbot_app  |     return await anext(self.gen)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 1064, in begin
taskbot_app  |     async with conn:
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/base.py", line 121, in __aenter__
taskbot_app  |     return await self.start(is_ctxmanager=True)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 274, in start
taskbot_app  |     await greenlet_spawn(self.sync_engine.connect)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
taskbot_app  |     result = context.throw(*sys.exc_info())
taskbot_app  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3274, in connect
taskbot_app  |     return self._connection_cls(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 146, in __init__
taskbot_app  |     self._dbapi_connection = engine.raw_connection()
taskbot_app  |                              ^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3298, in raw_connection
taskbot_app  |     return self.pool.connect()
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 449, in connect
taskbot_app  |     return _ConnectionFairy._checkout(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1263, in _checkout
taskbot_app  |     fairy = _ConnectionRecord.checkout(pool)
taskbot_app  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
taskbot_app  |     rec = pool._do_get()
taskbot_app  |           ^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 179, in _do_get
taskbot_app  |     with util.safe_reraise():
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
taskbot_app  |     raise exc_value.with_traceback(exc_tb)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
taskbot_app  |     return self._create_connection()
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 390, in _create_connection
taskbot_app  |     return _ConnectionRecord(self)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 674, in __init__
taskbot_app  |     self.__connect()
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 900, in __connect
taskbot_app  |     with util.safe_reraise():
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
taskbot_app  |     raise exc_value.with_traceback(exc_tb)
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 896, in __connect
taskbot_app  |     self.dbapi_connection = connection = pool._invoke_creator(self)
taskbot_app  |                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 646, in connect
taskbot_app  |     return dialect.connect(*cargs, **cparams)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 622, in connect
taskbot_app  |     return self.loaded_dbapi.connect(*cargs, **cparams)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 961, in connect
taskbot_app  |     await_only(creator_fn(*arg, **kw)),
taskbot_app  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
taskbot_app  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
taskbot_app  |     value = await result
taskbot_app  |             ^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connection.py", line 2421, in connect
taskbot_app  |     return await connect_utils._connect(
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1075, in _connect
taskbot_app  |     raise last_error or exceptions.TargetServerAttributeNotMatched(
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1049, in _connect
taskbot_app  |     conn = await _connect_addr(
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 886, in _connect_addr
taskbot_app  |     return await __connect_addr(params, True, *args)
taskbot_app  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 931, in __connect_addr
taskbot_app  |     tr, pr = await connector
taskbot_app  |              ^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 818, in _create_ssl_connection
taskbot_app  |     new_tr = await loop.start_tls(
taskbot_app  |              ^^^^^^^^^^^^^^^^^^^^^
taskbot_app  |   File "/usr/local/lib/python3.11/asyncio/base_events.py", line 1268, in start_tls
taskbot_app  |     await waiter
taskbot_app  |   File "/usr/local/lib/python3.11/asyncio/sslproto.py", line 578, in _on_handshake_complete
taskbot_app  |     raise handshake_exc
taskbot_app  | ConnectionResetError
