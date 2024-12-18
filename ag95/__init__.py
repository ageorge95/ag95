# ############## DecimalScripts #################
from .DecimalScripts.decimals_places import decimals_places
from .DecimalScripts.nr_normalisation import nr_normalisation
from .DecimalScripts.round_closer import (round_down_closer,
                                          round_up_closer)

# ############## LoggingScripts #################
from .LoggingScripts.custom_logger import (configure_logger,
                                           configure_loggers)

# ############## Threading #################
from .Threading.thread_monitor import ThreadMonitor

# ############## General #################
from .General.singleton_metaclass import (Singleton_with_cache,
                                          Singleton_without_cache)
from .General.stdin_watcher import stdin_watcher
from .General.filepaths_from_folderpath import extract_filenames_from_filepath
from .General.shorten_long_strings import shorten_long_str

# ############## TimeRelated #################
from .TimeRelated.format_from_seconds import format_from_seconds

# ############## SqliteDatabase #################
from .SqliteDatabase.SqLiteDbWrapper import (SqLiteDbWrapper,
                                             SqLiteColumnDef)
from .SqliteDatabase.SqLiteDbMigration import SqLiteDbMigration
from .SqliteDatabase.SqLiteDbBackup import SqLiteDbbackup

# ############## GenericDatabase #################
from .GenericDatabase.DbWrapper import (DbWrapper,
                                       ColumnDef)
from .GenericDatabase.DbMigration import DbMigration
from .GenericDatabase.DbBackup import Dbbackup

# ############## DuckDbDatabase #################
from .DuckDbDatabase.DuckDbWrapper import (DuckDbWrapper,
                                           DuckColumnDef)
from .DuckDbDatabase.DuckDbMigration import DuckDbMigration
from .DuckDbDatabase.DuckDbbackup import DuckDbbackup

# ############## PlotlyRelated #################
from .PlotlyRelated.PlotlyRelatedBase import (ScatterPlotDef,
                                              BarPlotDef,
                                              HistogramPlotDef,
                                              SinglePlot,
                                              MultiRowPlot)
from .TemplatesHtml.export_html_templates import export_html_templates

# ############## DataManipulation #################
from .DataManipulation.datetime_lists_normalise import datetime_lists_normalise

# ############## TradingRelated #################
from .TradingRelated.TrailingDecision import (TrailingDecision,
                                              MessagesTrailingDecision)

# ############## Cryptography #################
from .WindowsCredentials.windows_credentials import (save_password,
                                                     get_password,
                                                     delete_password)