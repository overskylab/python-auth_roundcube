#!/usr/bin/python
import re, random, time, urllib2
from robobrowser import RoboBrowser
from requests import Session

# Do not have slash (/) on last character
roundcube_url = 'https://domain.sample/roundcube'


def credentials():
    print '[+] Setting credentails'
    credentials = [
            {'username': 'username1', 'password': 'password1'},
            {'username': 'username2', 'password': 'password2'}
        ]
    return credentials


def main():
    print '[+] Initializing RoboBrowser'
    # session = Session()
    controller(new_browser(), credentials())


def new_browser():
    browser = RoboBrowser(
            history=True,
            # session=session,
            user_agent='RoboBrowser Testing',
            parser='html.parser'
        )
    return browser


def controller(browser, credentials):
    for credential in credentials:
        print '=> Current User: '+credential['username']
        login(browser, credential)
        verify(browser)

        logout(browser) # Clean
        
        # Random sleep_time to wait
        sleep_time = random.randint(2,4)
        print '[+] Sleeping for '+str(sleep_time)
        time.sleep(sleep_time)


def login(browser, credential):
    print '[+] Logging in...'
    browser.open(roundcube_url)
    form = browser.get_form()
    form['_url'] = '_task=login'
    form['_user'] = credential['username']
    form['_pass'] = credential['password']
    browser.submit_form(form)
    # print browser.select('html') # Debug


def logout(browser):
    try:
        # logout = browser.select('#rcmbtn108')
        # browser.follow_link(logout[0])
        browser.open(roundcube_url)
        form_logout = browser.get_forms()[1]
        token = form_logout['_token'].value
        url_logout = roundcube_url+'/?_task=logout&_token='+token
        browser.open(url_logout)
        print '[+] Logout successfully'
    except:
        print '[-] Cannot logout : Not login yet'


def verify(browser):
    if ( len(browser.select('#rcmloginsubmit')) == 0 and
         len(browser.select('.username')) != 0 ):
        print '[+] Login successfully'
    else:
        print '[-] Login failed'


main()
