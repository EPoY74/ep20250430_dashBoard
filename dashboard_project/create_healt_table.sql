CREATE TABLE server_health (
    id SERIAL PRIMARY KEY,
    ip TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT now(),

    channels_total INTEGER,
    channels_online INTEGER,
    cpu_load REAL,
    uptime INTEGER,

    disks_ok BOOLEAN,
    database_ok BOOLEAN,
    network_ok BOOLEAN,
    automation_ok BOOLEAN,

    disks_stat_main_days REAL,
    disks_stat_priv_days REAL,
    disks_stat_subs_days REAL,

    raw JSONB
);