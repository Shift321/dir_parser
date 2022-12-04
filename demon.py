import time

from main import main
from daemons.utils.config_reader import read_config
from daemons.utils.arg_parser import create_parser_for_daemon

parser = create_parser_for_daemon()
args = parser.parse_args()
data = read_config(args.config)

while True:
    main(data)
    time.sleep(15)

