from random import randint
from time import sleep

import uiautomator2 as u2

from adbutils import adb

import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def open_snack_video(d):
    # cmd = 'adb shell monkey -p com.kwai.bulldog -c android.intent.category.LAUNCHER 1'
    # cmd_res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding="utf8")
    logging.info("Opening Snack Video app...")
    d.app_start("com.kwai.bulldog", use_monkey=True, wait=True)
    logging.info(d.app_current())


def init_devicd():
    for d in adb.device_list():
        logging.info(d.serial)
    d = adb.device_list()[0].serial

    d = u2.connect(d)
    # d = u2.connect('192.168.43.1:5555')
    d.screen_on()
    return d


def open_tiktok(d):
    logging.info("Opening TikTok app...")
    d.app_start("com.zhiliaoapp.musically", use_monkey=True, wait=True)
    logging.info(d.app_current())


def crash_tiktok(d):
    logging.info("Closing Tiktok App...")
    d.screenshot("./logs/crash.jpg")
    d.app_stop("com.zhiliaoapp.musically")


def random_sleep(a, b):
    delay = randint(a, b)
    logging.info("Sleep for " + str(delay) + (delay == 1 and " second" or " seconds"))
    sleep(delay)


def unfollow_all(d):
    total_unfollowed = 0
    random_sleep(10, 15)
    try:
        # random_scroll = randint(0, 10)
        # logger.info(f'Skipping to {random_scroll} videos')
        # for i in range(random_scroll):
        #     random_sleep(10, 15)
        #     d().swipe('up')
        d(text="Profile").click()

        d().swipe('up')
        d().swipe('down')
        d().swipe('down')
        random_sleep(10, 15)
        d(text="Following").click()
        while total_unfollowed < 500:
            random_unfollow = randint(5, 10)
            for i in range(random_unfollow):
                try:
                    try:
                        d(text="Following").click()
                    except:
                        d(text="Friends").click()
                    total_unfollowed += 1
                    logging.info(f"{total_unfollowed} accounts unfollowed")
                except:
                    logging.info("Scrolling down to get more accounts")
                    d().scroll()
                random_sleep(2, 5)
            random_sleep(5, 10)
            logging.info("Scrolling down to get more accounts")
            d().scroll()
    except:
        crash_tiktok(d)
    logger.info(f"Script Completed, total followed {total_unfollowed}")


def random_follow(d):
    total_followed = 0
    try:
        random_scroll = randint(0, 10)
        logger.info(f'Skipping to {random_scroll} videos')
        for i in range(random_scroll):
            random_sleep(10, 15)
            d().swipe('up')
        d.swipe_ext("left")

        d().swipe('up')
        d().swipe('down')
        d().swipe('down')
        random_sleep(10, 15)
        d(text="Followers").click()
        while total_followed < 100:
            random_follow = randint(5, 10)
            for i in range(random_follow):
                try:
                    d(text="Follow").click()
                    total_followed += 1
                    logging.info(f"{total_followed} accounts followed")
                except:
                    logging.info("Scrolling down to get more accounts")
                    d().scroll()
                random_sleep(2, 5)
            random_sleep(5, 10)
            logging.info("Scrolling down to get more accounts")
            d().scroll()
    except:
        crash_tiktok(d)
    logger.info(f"Script Completed, total followed {total_followed}")


def random_sleep_long():
    delay = randint(25, 30)
    logging.info("Sleep for " + str(delay) + (delay == 1 and " second" or " seconds"))
    sleep(delay)


def like_tiktok(d):
    # pre_like = int(d(resourceId="com.zhiliaoapp.musically:id/aas").get_text())
    follow_chance = randint(1, 100)
    if follow_chance > (100 - 30):
        logging.info("like" + str(follow_chance))
        d(className="android.widget.FrameLayout",
          resourceId="com.zhiliaoapp.musically:id/aar").click()
        # after_like = int(
        #     d(resourceId="com.zhiliaoapp.musically:id/aas").get_text())

        # if after_like != pre_like:
        # storage.add_interacted_user(
        #     d(resourceId="com.zhiliaoapp.musically:id/title").get_text(), liked=True)

    scroll = d.xpath(
        '//android.support.v4.view.ViewPager').info.get('bounds').get('bottom') * 3 / 4
    d.swipe(0, int(scroll), 0, 0, 0.08)
    d(resourceId="com.zhiliaoapp.musically:id/a2g").wait_gone(timeout=10.0)


if __name__ == '__main__':
    logger = logging.getLogger()

    d = init_devicd()
    open_tiktok(d)
    # unfollow_all(d)
    while True:
        open_tiktok(d)
        random_follow(d)
        random_sleep(180, 360)
        crash_tiktok(d)
        logging.info('Finish')
