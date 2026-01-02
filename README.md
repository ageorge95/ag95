# ag95
Repository for common code used in some of my other repos. Compatible with python 3.13.x

Currently ag95 has the following modules and utilities.:

<table border="1" cellspacing="0" cellpadding="5">
  <thead>    
    <tr>
      <th>Module</th>
      <th>Utility</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <!-- all group -->
    <tr>
      <td>all</td>
      <td>-</td>
      <td>Will install all dependencies.</td>
    </tr>
    <!-- DecimalScripts group -->
    <tr>
      <td rowspan="3">DecimalScripts</td>
      <td>decimals_places</td>
      <td>Returns the number of decimal places for a given float.</td>
    </tr>
    <tr>
      <td>nr_normalisation</td>
      <td>Normalizes a float to a specified number of decimal places without rounding.</td>
    </tr>
    <tr>
      <td>round_[up/down]_closer</td>
      <td>Rounds a float up or down to its last decimal position.</td>
    </tr>
    <!-- LoggingScripts group -->
    <tr>
      <td>LoggingScripts</td>
      <td>configure_[logger/loggers]</td>
      <td>Provides a custom logging solution with numerous quality-of-life features.</td>
    </tr>
    <!-- Threading group -->
    <tr>
      <td>Threading</td>
      <td>ThreadMonitor</td>
      <td>Monitors a list of threads until they complete, then notifies upon completion.</td>
    </tr>
    <!-- General group -->
    <tr>
      <td rowspan="4">General</td>
      <td>extract_filenames_from_folderpath</td>
      <td>Recursively extracts filenames from a folder, filtering by file extension.</td>
    </tr>
    <tr>
      <td>shorten_long_str</td>
      <td>Shortens long strings by inserting an asterisk in the middle.</td>
    </tr>
    <tr>
      <td>Singleton_[with/without]_cache</td>
      <td>Provides a metaclass for creating singleton classes with optional caching capabilities.</td>
    </tr>
    <tr>
      <td>stdin_watcher</td>
      <td>Monitors standard input and triggers configurable actions based on specified keywords.</td>
    </tr>    
    <!-- TimeRelated group -->
    <tr>
      <td rowspan="2">TimeRelated</td>
      <td>format_from_seconds</td>
      <td>Formats elapsed time (in seconds) into a human-readable string with configurable granularity.</td>
    </tr>
    <tr>
      <td>TimerContext</td>
      <td>Context manager for measuring the execution time of code blocks.</td>
    </tr>
    <!-- SqliteDatabase group -->
    <tr>
      <td rowspan="3">SqliteDatabase</td>
      <td>SqLiteDbbackup</td>
      <td>Creates backups of SQLite databases.</td>
    </tr>
    <tr>
      <td>SqLiteDbMigration</td>
      <td>Performs schema migrations on SQLite databases.</td>
    </tr>
    <tr>
      <td>SqLiteDbWrapper</td>
      <td>Offers utilities for managing and manipulating SQLite databases.</td>
    </tr>
    <!-- SqliteDatabaseService group -->
    <tr>
      <td rowspan="1">SqLiteDbWrapperService</td>
      <td>SqLiteDbWrapperService</td>
      <td>Flask service served by waitress that wraps all the SqliteDb methods in a highly efficient manner.</td>
    </tr>
    <!-- GenericDatabase group -->
    <tr>
      <td rowspan="3">GenericDatabase</td>
      <td>Dbbackup</td>
      <td>Creates backups of generic databases (e.g., SQLite).</td>
    </tr>
    <tr>
      <td>DbMigration</td>
      <td>Performs schema migrations on generic databases (e.g., SQLite).</td>
    </tr>
    <tr>
      <td>DbWrapper</td>
      <td>Provides utilities for managing and manipulating generic databases (e.g., SQLite).</td>
    </tr>
    <!-- DuckDbDatabase group -->
    <tr>
      <td rowspan="3">DuckDbDatabase</td>
      <td>DuckDbbackup</td>
      <td>Creates backups of DuckDB databases.</td>
    </tr>
    <tr>
      <td>DuckDbMigration</td>
      <td>Performs schema migrations on DuckDB databases.</td>
    </tr>
    <tr>
      <td>DuckDbWrapper</td>
      <td>Offers utilities for managing and manipulating DuckDB databases.</td>
    </tr>
    <!-- PlotlyRelated group -->
    <tr>
      <td rowspan="5">PlotlyRelated</td>
      <td>SinglePlot</td>
      <td>Constructs a Plotly figure featuring a single plot.</td>
    </tr>
    <tr>
      <td>MultiRowPlot</td>
      <td>Creates a Plotly figure with multiple subplots arranged in rows.</td>
    </tr>
    <tr>
      <td>BarPlotDef</td>
      <td>Definition class for configuring bar plots in Plotly.</td>
    </tr>
    <tr>
      <td>HistogramPlotDef</td>
      <td>Definition class for configuring histogram plots in Plotly.</td>
    </tr>
    <tr>
      <td>ScatterPlotDef</td>
      <td>Definition class for configuring scatter plots in Plotly.</td>
    </tr>
    <!-- TemplatesHtml group -->
    <tr>
      <td>TemplatesHtml</td>
      <td>export_html_templates</td>
      <td>Exports ready-to-use HTML templates, particularly useful for Django frameworks.</td>
    </tr>
    <!-- DataManipulation group -->
    <tr>
      <td>DataManipulation</td>
      <td>datetime_lists_normalise</td>
      <td>Normalizes multiple datetime lists into a unified list with configurable constraints.</td>
    </tr>
    <!-- TradingRelated group -->
    <tr>
      <td>TradingRelated</td>
      <td>TrailingDecision</td>
      <td>Implements a trailing mechanism to automate buy/sell decisions based on configurable thresholds.</td>
    </tr>
    <!-- WindowsCredentials group -->
    <tr>
      <td rowspan="3">WindowsCredentials</td>
      <td>save_password</td>
      <td>Saves passwords securely to the Windows Credential Manager.</td>
    </tr>
    <tr>
      <td>get_password</td>
      <td>Retrieves passwords from the Windows Credential Manager.</td>
    </tr>
    <tr>
      <td>delete_password</td>
      <td>Deletes a specified password from the Windows Credential Manager.</td>
    </tr>
    <!-- IoT group -->
    <tr>
      <td rowspan="2">IoT</td>
      <td>TuyaCloudControl</td>
      <td>Wrapper for managing and reading Tuya devices via the Tuya Cloud.</td>
    </tr>
    <tr>
      <td>SmartThingsControl</td>
      <td>Wrapper for managing and reading SmartThings devices via the SmartThings Cloud.</td>
    </tr>
    <!-- IO group -->
    <tr>
      <td>IO</td>
      <td>single_file_transfer</td>
      <td>Highly scalable utility for parallel file transfers using chunk segmentation.</td>
    </tr>
    <!-- Colors group -->
    <tr>
      <td>Colors</td>
      <td>red_green_from_range_value</td>
      <td>Will output a rgb value between green and red based on a given value, a minimum and a maximum.</td>
    </tr> 
    <!-- EmailHandler group -->
    <tr>
      <td>EmailHandler</td>
      <td>send_mail_from_gmail</td>
      <td>Will send an email using a gmail account.</td>
    </tr> 
  </tbody>
</table>

# Deploy this code in your repositories
You can quickly access the stuff by

  - use this repo as a submodule (instructions on how to setup git sub-modules can be found here: https://git-scm.com/book/en/v2/Git-Tools-Submodules)
  
  - install this repo as a package with pip
  
    - to install the barebone package with no extra dependencies (not recommended as some stuff may not work in this way) you can use `python -m pip install git+https://github.com/ageorge95/ag95.git`
   
    - to install the package with extra dependencies specific to your usecase you can use a syntax like this (for older pip versions) `python -m pip install git+https://github.com/ageorge95/ag95.git#egg=ag95[DecimalScripts,SqliteDatabase]` or (for newer pip versions) `python -m pip install "ag95[DecimalScripts,SqliteDatabase] @ git+https://github.com/ageorge95/ag95.git"`
  
    - to upgrade the package you would simply have to use the commands above and add the `--upgrade` flag, for example: `python -m pip install --upgrade git+https://github.com/ageorge95/ag95.git`
   
    - NOTE1: the `extras_require` mechanism was recently introduced as ag95 has grown and contains lots of different parts and some of them do not even require an external dependency while some require multiple dependencies, which slowed time the installation of ag95 considerably. Now, with `extras_require`, you have to specify exactly which part/ parts of ag95 you will plan to use => the installation is as fast as possible for your particular use cases.
   
    - NOTE2: in the future I might provide wheels for this package, but for now there is not a great need for them.

# Support
Found this project useful? Send your ❤ in any form you can 🙂. Please contact me if you donated and want to be added to the contributors list !

- apple APPLE---apple1tdscevmlwa03rt464mr03tf6qs6y2xm3ay4z9lzn9pshad6jkp2s4crqd9
- goldcoin OZT---ozt1u8klct3kcluvmu9hha8w6vte70d2z37zy7zydz55gygper0658rqkjqwts
- salvia XSLV---xslv19j3zexpgels2k8fkp30phxpxxz6syfzq52t2tuy8ac50nfmnennse9vjcw
- chia XCH---xch1glz7ufrfw9xfp5rnlxxh9mt9vk9yc8yjseet5c6u0mmykq8cpseqna6494
- cryptodoge XCD---xcd1ds6jljkla5gwfjgty8w4q442uznmw9erwmwnvfspulqke3ya9nxqy9fe8t
- flax XFX---xfx13uwa4zqp0ah5740mknk0z8g3ejdl06sqq8ldvvk90tw058yy447saqjg3u
- cannabis CANS---cans16ur4nqvvtdr8yduum5pljr3a73q33uuage6ktnsdr579xeerkc5q604j5v
- wheat WHEAT---wheat1z4cz3434w48qumwt2f2dqtmgq4lfyv5aswmda7yfmamhml2afrzsa80mr2
- melati XMX---xmx1am6cjj5hrvwhjt8nvuytf2llnjhklpuzcjr4ywg7fe0n7a7n3tns3dj3jf
- taco XTX---xtx1crayqhdtx2rs5680q65c0c2ndaltje6vem0u0nnxtks4ucy058uqc0ak8m
- greendoge GDOG---gdog1ry524dunyuxkrjmzrdrgf5y6hzcdl0fghmncfcxxl83jknn82kmstzjjxk
- tad TAD---tad19s5nxa04znxsl7j6hud8p0uqtmnwd770d5a3nz40dtgwnuufjz0sgfcpnx
- avocado AVO---avo1x9z98u6jkynkwutwd49cd58enqh3qfwlc3l7mamx2r6hgxdgqphs88t3yn
- spare SPARE---spare12e68ghay27pcdyuqcaz5qvtwst5mxzht33nxsxmygcd8nnxzhj6qjzytex
- cactus CAC---cac189er7g8gfsr6yl40t6gq8qygcrsjxkzhp50sk2xa6wh0f2nxzrhsm6rkfe
- flora XFL---xfl149k04h5p9crzsl0xz50efzka9clt56xtg5h33l35m8ld9h2knhqqvs7u76
- kale XKA---xka1m7hskvcd8xqx0a2e5nxc3ldn8gcz83pwvlkgd5x8vflaaq3uetmqj0ztk5
- maize XMZ---xmz1ycj7x6tsajgyannvr92udj23dsj6l4syqx38pmpzf6e7kkeeuvysscdvyw
- hddcoin HDD---hdd1qfs8hdtdrmsw9ya04cjex0d6dzkn7lfv7vp9g2dgup3p87ye9gqs6zvam2
- dogechia XDG---xdg17g6zx3u2a2zslwxrm0spv2297ygnuzhyme89x8kd5mrjz7mns39q6ge64c
- nchain ext9 NCH---nch1ae8hujcantv7naes30etvvcssm6uak9xzd5edwhtyq05adt60hkqlgyfmz
- chives XCC---xcc1amn5txlltvlcnlt6auw24ys6xku7t3npqt2szllassymswnehepszhnjar
- BTCGreen xBTC---xbtc1njnsnayxuj4nn0fnzf2nsjnladh79spljx5vvs8v6vqhk9kp6rksgvyszh
- Pipscoin PIPS---pips13qcawq6y5dkxqtwnup04m2zmee9lpzsec0zyczt0pd0ra6cuut3qgvhj0k
- mint XKM---xkm1k0nkq575wm3nmtkkxwrfmxg7qpt0hxe5m2fvw0dgvw3q0ynmzn3qqu5ntf
- stor STOR---stor1vahvcz80arp2jl6v4np8grjxncrypzfelmm4uk0gvds5rpuf523qn9w482
- tranzact  TRZ---trz1mct7p22g2m9gn9m0xtuac4mnrwjkev0pqsxgx7tr6cjk2thnxmkq8q45ep
- Staicoin STAI---stai1m0axlhek947j5mz2wpvy0m9sky49h3jfqwqesy8rmzxfv9j9k5kq9zl6ft
- Venidium XVM---xvm1h35hgaqxyvrgjmmr2qgr48ft0cxltyhnge6zkwkfsl9x93d4uq2qq9la0k
- Skynet XNT---xnt1cq8xdu8svwhruefr5khzpqxturemtqrf6gk7uqjyjrhdl2dyapmsh9desg
- Shibgreen XSHIB---xshib1pkelrz8uml46m6hdw06ttezhaqasexe0527jce4cc03uj4fc8rcsaaatwy
- Silicoin SIT---sit1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrqj0s60a
- bpx BPX---bpx10d25g8jechcs2rfstkzpj2rzt68skw4etvqm2j7f8545uzd6kyrqgr2ea8
- Gold GL---gl1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrqqwx0ye
- joker---xjk1may9ee07y0yf0a5k3hvhq54wem07ny5k7grzksgm4rnhl3yzwnqss8lsge
- profit---profit1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrqfhghvg
- littlelambocoin LLC---llc1wfhhxn4dtr7luedc4lzld2y2q32r66ruvqyppj7vr6g5u75xn92s3pz9gw
- ecostake ECO---eco1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrq5l9vpy
- chinilla HCX---hcx16ce9d6pj80nw6j2j9hgax30k6ww43na3ve86pm87tecsdhgc03sq7cvnmt
- petroleum XPT---xpt1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrqq2qcs2
- Scam SCM---scm1m3sh0pxvjcen2hyzmjgayac0x55ljhlwrptqu90thp6mtpfngx6qgkjwht
- seno XSE---xse1jx8mvumy9243t8qcu0e476r0azvckyaeyhnmu6jswxcr57q09zyqla5w2a
- lucky SIX---six1r09eundsl9ntdw5vgq9xk9qedcvxdg7tg3urndcewppc3cn55p2syhu2d4
- moon---moc1k49pfczryvea0h3hf6ls2fm6gykhaa9jymfhuy27790f470rt8js770rdv
- lotus LCH---lch1yxmdv2jykwsvmwemka3uc2g3zg7dqfaevd8n2z2jht9nstsammtsyla2ex
- Coffee XCF---xcf1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrqcq54t6
- ethgreen XETH---xeth1e24uzser8h78gun2jppnqsgx7vsrktzkgdeuknat63ppcfw7htuq2pu73a
- goji XGJ---xgj1x0xyfmkz0xylyaaq6360un9hydjc543lrtuwu9pk5d008acq939qrlgdut
- greenbtc GBTC---gbtc1df3l4xpzc65xyzvdlleww6stwt70kd9a4ra0836hf6ahpcwd7yrqw0awqh
