import argparse
import traceback

import asyncio
import aiodns
# import tempfile

from helpers import extract_ips


async def check_bot(resolver, ip):
    """Check if bot is ok"""

    good_domains = [
        "yandex.com",
        "google.com",
        "yandex.net",
        "yandex.ru",
        "googlebot.com",
    ]
    try:
        result = await resolver.gethostbyaddr(ip)
    except:
        print("CAN'T Resolve:", ip)
        print(traceback.format_exc())
        return False

    if not result:
        print(f"Bad bot: {ip}")
        return

    good = False
    for d in good_domains:
        if result.name.endswith(d):
            good = True
    if not good:
        print(f"Bad bot: {ip}")
    else:
        print(f"Good bot: {ip}")


async def run(args):
    """Main function: parse log file"""

    resolver = aiodns.DNSResolver(loop=loop)

    block_size = 200
    filename = args.filename
    ips = extract_ips(filename).split("\n")
    if args.debug:
        print("Total IP's:", len(ips))

    rs = []
    for ip in ips:
        if not ip.strip() == "":
            check_task = check_bot(resolver, ip)
            t = asyncio.create_task(check_task)
            rs.append(t)

    await asyncio.gather(*rs)
    await asyncio.sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="FakeBots Parser",
        description="This programm parse webserver's logs for fake SE bots",
    )
    parser.add_argument("filename")
    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        dest="debug",
        action="store_true",
        help="Verbose and debug output",
    )
    args = parser.parse_args()
    print(args)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(args))
    loop.run_until_complete(future)
