import api
import utils
import json
import sched
import datetime
import time
import run


def main():
    with open("../fx_config.json") as config_buffer:
        config = json.loads(config_buffer.read())

    oanda = api.oanda(
        config["accounts"]["accessToken"],
        config["accounts"]["accountId"],
        config["accounts"]["domain_type"],
        config["api"]["instrument"],
        config["api"]["units"],
        config["api"]["granularity"],
        config["api"]["UpperBound_tickets"],
    )

    scheduler = sched.scheduler(time.time, time.sleep)

    while(1):
        next_time = utils.get_next(config["api"]['granularity'])
        print("\nnext : {0}".format(next_time))
        run_at = datetime.datetime.strptime(next_time, '%Y-%m-%d %H:%M:%S')
        run_at = int(time.mktime(run_at.utctimetuple()))
        scheduler.enterabs(run_at, 1, run.processing,  kwargs={'api': oanda})
        scheduler.run()


if __name__ == "__main__":
    main()
