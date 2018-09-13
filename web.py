#!/usr/bin/env python3
from flask import Flask, redirect, url_for, flash
from flask import render_template
from flask import request
from aoss import loginOS, ports, vlan
import json
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

disable_warnings(InsecureRequestWarning)

#
# This section is no longer used. Please go to http://127.0.0.1:5000/config
# to configure this web frontend. You can also edit config.json, though
# the above web frontend is best.
#

# Open config file for usernae, password, switch, ignored vlans, etc
with open('config.json') as lf:
    data = json.load(lf)

app = Flask(__name__)
app.secret_key = 'EF657435D29A74A40A96B5AF3792AD0D322BE69EAC77DFE13CF23B3B46201970'

@app.route('/get_ports')
def get_ports():
    # data = {"user": username, "password": password, "ipadd": switch_ip}
    with open('config.json') as lf:
        data = json.load(lf)
    baseurl = "https://{}/rest/v4/".format(data['ipadd'])
    cookie_header = loginOS.login_os(data, baseurl)

    listvlans = vlan.get_vlan(baseurl, cookie_header)['vlan_element']
    listports = ports.get_ports(baseurl, cookie_header)
    listvlansports = vlan.get_vlans_ports(baseurl, cookie_header)

    useablevlans = []
    for lvlan in listvlans:
        if str(lvlan['vlan_id']) not in data['ignored_vlans']:
            useablevlans.append({'vlan_id': lvlan['vlan_id'], 'vlan_name': lvlan['name']})


    def test_get_ports():
        cookie_header = loginOS.login_os(data, baseurl)
        loginOS.logout(baseurl, cookie_header)

    numberofports = listports['collection_result']['total_elements_count']
    loginOS.logout(baseurl, cookie_header)


    port_status = data['port_status']
    title = data['title']
    return render_template('ports.html', title=title, ports=listports['port_element'],
                           listvlansports=listvlansports['vlan_port_element'],
                           vlans=listvlans, numofports=numberofports,
                           useablevlans=useablevlans, port_status=port_status, data=data)


@app.route("/")
def root():
    title=data['title']
    return render_template('index.html', title=title)

@app.route('/portsetup')
def port_setup():
    results = "Port Config"
    return render_template('port_setup.html', title='Port Configuration', results=results)

@app.route('/ivlan_config', methods=['GET', 'POST'])
def ivlan_config():
    if request.method == 'POST':
        with open('config.json') as f:
            data = json.load(f)
        baseurl = "https://{}/rest/v4/".format(data['ipadd'])
        cookie_header = loginOS.login_os(data, baseurl)
        loginOS.logout(baseurl, cookie_header)

        ivlans = request.form.getlist('ivlans')

        newdata = {}
        newdata['user'] = data['user']
        newdata['password'] = data['password']
        newdata['ipadd'] = data['ipadd']
        newdata['title'] = data['title']
        newdata['ignored_vlans'] = ivlans
        newdata['port_status'] = data['port_status']
        newdata['port_start'] = data['port_start']
        newdata['port_end'] = data['port_end']


        with open('config.json', 'w') as fp:
            json.dump(newdata, fp)

        flash('Ignored VLANS successfully updated')

    with open('config.json') as f:
        data = json.load(f)
    baseurl = "https://{}/rest/v4/".format(data['ipadd'])
    cookie_header = loginOS.login_os(data, baseurl)

    listvlans = vlan.get_vlan(baseurl, cookie_header)['vlan_element']
    loginOS.logout(baseurl, cookie_header)

    av = []
    for lv in listvlans:
            av.append(lv['vlan_id'])

    ignored = list(map(int, data['ignored_vlans']))
    av_c = {}
    for a in av:
        if a in ignored:
                av_c[a] = True
        else:
            av_c[a] = False

    return render_template('ivlan_config.html', title='Config Demo', data=data, ignored=ignored, allvlans=listvlans, avc=av_c)



@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        with open('config.json') as f:
            data = json.load(f)

        newdata = {}
        user = request.form.get('user')
        port_status = request.form.get('port_status')
        ipadd = request.form.get('ipadd')
        title = request.form.get('title')
        ivlans = request.form.getlist('ivlans')
        if request.form.get('password') is None or request.form.get('password') == "":
            password = data['password']
        else:
            password = request.form.getlist('password')
        newdata['port_start'] = request.form.get('port_start')
        newdata['port_end'] = request.form.get('port_end')

        newdata['user'] = user
        newdata['password'] = password
        newdata['ipadd'] = ipadd
        newdata['title'] = title
        newdata['ignored_vlans'] = data['ignored_vlans']
        newdata['port_status'] = port_status


        with open('config.json', 'w') as fp:
            json.dump(newdata, fp)

        flash('Configuration successfully updated')

    with open('config.json') as f:
        data = json.load(f)


    return render_template('config.html', title='Config Demo', data=data)


@app.route('/port_update', methods=['GET', 'POST'])
def port_update():
    # data = {"user": user, "password": password, "ipadd": switch_ip}
    baseurl = "https://{}/rest/v4/".format(data['ipadd'])
    cookie_header = loginOS.login_os(data, baseurl)

    if request.method == 'POST':
        requestmethod = request.form
        port_id = request.form.get('port_id')
        newvlan = int(request.form.get('newvlan'))
        # {'vlan_id': 102, 'port_id': 'trk1', 'port_mode': 'POM_TAGGED_STATIC'},

        vlanport = {'vlan_id': newvlan, 'port_id': port_id, 'port_mode': 'POM_UNTAGGED'}
        response = vlan.create_vlan_with_port(baseurl, vlanport, cookie_header)
        title = "Port Config"

    loginOS.logout(baseurl, cookie_header)
    return redirect(url_for('get_ports', title=title))
    # return render_template('port_setup.html', title='Port Configuration', results=results)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
