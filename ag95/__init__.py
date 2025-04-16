# ############## DecimalScripts #################
try:
    from .DecimalScripts.decimals_places import decimals_places
    from .DecimalScripts.nr_normalisation import nr_normalisation
    from .DecimalScripts.round_closer import (round_down_closer,
                                              round_up_closer)
except:
    pass

# ############## LoggingScripts #################
try:
    from .LoggingScripts.custom_logger import (configure_logger,
                                               configure_loggers)
except:
    pass

# ############## Threading #################
try:
    from .Threading.thread_monitor import ThreadMonitor
except:
    pass

# ############## General #################
try:
    from .General.singleton_metaclass import (Singleton_with_cache,
                                              Singleton_without_cache)
    from .General.stdin_watcher import stdin_watcher
    from .General.filepaths_from_folderpath import extract_filenames_from_filepath
    from .General.filepaths_from_folderpath import extract_filenames_from_folderpath
    from .General.shorten_long_strings import shorten_long_str
except:
    pass

# ############## TimeRelated #################
try:
    from .TimeRelated.format_from_seconds import format_from_seconds
    from .TimeRelated.timer_context import TimerContext
except:
    pass

# ############## SqliteDatabase #################
try:
    from .SqliteDatabase.SqLiteDbWrapper import (SqLiteDbWrapper,
                                                 SqLiteColumnDef)
    from .SqliteDatabase.SqLiteDbMigration import SqLiteDbMigration
    from .SqliteDatabase.SqLiteDbBackup import SqLiteDbbackup
except:
    pass

# ############## GenericDatabase #################
try:
    from .GenericDatabase.DbWrapper import (DbWrapper,
                                           ColumnDef)
    from .GenericDatabase.DbMigration import DbMigration
    from .GenericDatabase.DbBackup import Dbbackup
except:
    pass

# ############## DuckDbDatabase #################
try:
    from .DuckDbDatabase.DuckDbWrapper import (DuckDbWrapper,
                                               DuckColumnDef)
    from .DuckDbDatabase.DuckDbMigration import DuckDbMigration
    from .DuckDbDatabase.DuckDbbackup import DuckDbbackup
except:
    pass

# ############## PlotlyRelated #################
try:
    from .PlotlyRelated.PlotlyRelatedBase import (ScatterPlotDef,
                                                  BarPlotDef,
                                                  HistogramPlotDef,
                                                  SinglePlot,
                                                  MultiRowPlot)
    from .TemplatesHtml.export_html_templates import export_html_templates
except:
    pass

# ############## DataManipulation #################
try:
    from .DataManipulation.datetime_lists_normalise import datetime_lists_normalise
except:
    pass

# ############## TradingRelated #################
try:
    from .TradingRelated.TrailingDecision import (TrailingDecision,
                                                  MessagesTrailingDecision)
except:
    pass

# ############## Cryptography #################
try:
    from .WindowsCredentials.windows_credentials import (save_password,
                                                         get_password,
                                                         delete_password)
except:
    pass

# ############## IoT #################
try:
    from .IoT.SmartThings import SmartThingsControl
    from .IoT.TuyaCloud import TuyaCloudControl
except:
    pass

# ############## IO #################
try:
    from .IO.paralel_file_transfer import single_file_transfer
except:
    pass

# ############## Colors #################
try:
    from .Colors.rgb_from_range_value import red_green_from_range_value
except:
    pass

# ############## EmailHandler #################
try:
    from .EmailHandler.gmail import send_mail_from_gmail
except:
    pass