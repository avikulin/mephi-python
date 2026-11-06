from dz_simple_database_vikulin_m25_555.command.concreete.db_create_table import DbCommandCreateTable
from dz_simple_database_vikulin_m25_555.command.concreete.db_delete_command import DbCommandDelete
from dz_simple_database_vikulin_m25_555.command.concreete.db_drop_table import DbCommandDropTable
from dz_simple_database_vikulin_m25_555.command.concreete.db_insert_command import DbCommandInsert
from dz_simple_database_vikulin_m25_555.command.concreete.db_select_command import DbCommandSelect
from dz_simple_database_vikulin_m25_555.command.concreete.db_table_info import DbCommandTableInfo
from dz_simple_database_vikulin_m25_555.command.concreete.db_table_list import DbCommandTableList
from dz_simple_database_vikulin_m25_555.command.concreete.db_update_command import DbCommandUpdate
from dz_simple_database_vikulin_m25_555.command.factory.db_command_factory import DbCommandFactory
from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore

global_config = DbConfig()
metadata = DbMetadataStore(global_config)

command_factory = DbCommandFactory()
command_factory.register_command("^select\\s+from.+$",
                                 DbCommandSelect(metadata))
command_factory.register_command("^insert\\s+into\\s+\\w+\\s+values\\s*\\((.+)\\)$",
                                 DbCommandInsert(metadata))
command_factory.register_command("^update\\s+\\w+\\s+set(.+)$",
                                 DbCommandUpdate(metadata))
command_factory.register_command("^delete\\s+from\\s+\\w+\\s+where(.+)$",
                                 DbCommandDelete(metadata))
command_factory.register_command("^create\\s+table\\s+\\w+\\s*\\((.+)\\)$",
                                 DbCommandCreateTable(metadata))
command_factory.register_command("^drop\\s+table\\s+\\w+$",
                                 DbCommandDropTable(metadata))
command_factory.register_command("^table\\s+list$",
                                 DbCommandTableList(metadata))
command_factory.register_command("^table\\s+info\\s+\\w+$",
                                 DbCommandTableInfo(metadata))

