"""
{
    "disks": "1",
    "database": "1",
    "channels_total": "26",
    "channels_online": "26",
    "uptime": "421839",
    "cpu_load": "32.89",
    "network": "1",
    "automation": "1",
    "disks_stat_main_days": "52.12",
    "disks_stat_priv_days": "0.00",
    "disks_stat_subs_days": "14.42",
}

Шаг1
https://10.1.15.115:8080/login?username=***&password=***
Шаг2
https://10.1.15.115:8080/health?sid=tQYrWWmt # Запрос здоровья

https://10.1.15.115:8080/settings/network_interfaces/hostname?sid=EEPnwWL4 # Запрос названия сервера

https://10.1.15.115:8080/settings/?sid=EEPnwWL4 # Запрос  настроек сервера



Ответ о здоровье сервера:
{
	"disks": "1",
	"database": "1",
	"channels_total": "27",
	"channels_online": "27",
	"uptime": "370733",
	"cpu_load": "48.72",
	"network": "1",
	"automation": "1",
	"disks_stat_main_days": "32.00",
	"disks_stat_priv_days": "0.00",
	"disks_stat_subs_days": "14.05"
}
"""