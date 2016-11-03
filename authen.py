#!/usr/bin/python
import re, random, time, urllib2
from robobrowser import RoboBrowser
from requests import Session
from datetime import datetime, timedelta
from generate import Generate, vb_script


## Global config variable
roundcube_url = 'https://sample.domain/roundcube'

## Important variable!!!
mail_priviledge = 0


def credentials():
    '''
    Function to assign username and password
    '''
    generate = Generate()
    print '[+] Setting credentails'
    credentials = [
            {'username': 'sample@domain.com', 'password': 'sample'},
            #{'username': 'sample@domain.com', 'password': ''}
        ]
    for credential in credentials:
        if not credential['password']:
            credential.update({ 'password': str(generate.password(6)) })
    return credentials


def main():
    '''
    Main function to control workflow
    '''
    print '[+] Initializing RoboBrowser'
    # session = Session()
    controller(new_browser(), credentials())

    # To generate vbs code for excel script
    print generate_script(credentials(), mail_priviledge)


def new_browser():
    '''
    Function to create browser worker
    '''
    browser = RoboBrowser(
            history=True,
            # session=session,
            user_agent='RoboBrowser Testing',
            parser='html.parser'
        )
    return browser


def controller(browser, credentials):
    '''
    Manage browser to authen with RoundCube
    '''
    for credential in credentials:
        print '=> Current User: '+credential['username']
        print '=> Current Password: '+credential['password']

        login(browser, credential)
        verify(browser)
        logout(browser) # Clean
        
        # Random sleep_time to wait
        sleep_time = random.randint(1,3)
        print '[+] Sleeping for '+str(sleep_time)
        time.sleep(sleep_time)


def login(browser, credential):
    '''
    Login to RoundCube with sevaral parameters with browser
    '''
    print '[+] Logging in...'
    browser.open(roundcube_url)
    form = browser.get_form()
    form['_url'] = '_task=login'
    form['_user'] = credential['username']
    form['_pass'] = credential['password']
    browser.submit_form(form)
    # print browser.select('html') # Debug


def logout(browser):
    '''
    Function to logout from RoundCube web sites
    '''
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
        print '[!] Cannot logout : Not login yet OR stuck with capcha'


def verify(browser):
    '''
    For verify authentication
    Error or Failed from login sometime may be cause of Many attemp to login
    You can check via testing login by Browser on your computer (Manually)
    '''
    if ( len(browser.select('#rcmloginsubmit')) == 0 and
         len(browser.select('.username')) != 0 ):
        print '[+] Login successfully'
    else:
        print '[-] Login failed'


def generate_script(credentials, priviledge):
    '''
    Generate code for Excel VBS script to match with company policy
    This function need to import vb_script from Generate.py
    '''
    if len(credentials)==1:
        filename = credentials[0]['username'] + str(datetime.now().strftime("_%d%m%Y")) # username_<date_created>
    else:
        filename = ((credentials[0]['username']).split('@'))[1] + str(datetime.now().strftime("_%d%m%Y")) # domain_<date_created>
       
    print '[+] VBS script generating...'
    if priviledge==0:
        print '[!] For Normal user'
        time_result = datetime.now() + timedelta(days=+5)
        print '[+] Expired on '+ str(time_result.strftime("%d/%m/%Y"))
    else:
        print '[!] For Postmaster'
        time_result = datetime.now() + timedelta(days=+7)
        print '[+] Expired on '+ filename
    print '[+] Filename: '+ filename
    print '########################################'
    vbs = vb_script()
    for credential in credentials:
        vbs.add_user(credential['username'], credential['password'])
    code = vbs.gen_script(priviledge)
    code += '\n########################################'
    return code


main()
