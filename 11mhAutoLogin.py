# -*- coding:utf-8 -*-
# pip3 install requests
import re
import requests
import sys

if len(sys.argv) != 4:
    print("USAGE: python3 11mhAutoLogin.py <username> <password> <todaysay>")
    sys.exit(1)
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
TODAYSAY = sys.argv[3]

url = r'http://www.11mh.net/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
rex_formhash = r'<input type="hidden" name="formhash" value="(.*?)" />'
rex_sign = '<div class="c">\r\n(.*?) </div>'


def getFormHash(str):
    print(str)
    pattern = re.compile(rex_formhash)
    match = pattern.search(str)
    ret = ''
    if match:
        ret = match.group(1)
    return ret


class User11:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.host = "http://www.11mh.net"
        self.session = requests.session()

    def doLogin(self):
        loginUrl = self.host + "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
        data = {
            "username": self.username,
            "password": self.password,
            "quickforward": "yes",
            "handlekey": "ls"
        }
        ret = self.session.post(loginUrl, data)
        match = re.compile("window.location.href='(.*?)';").search(ret.text)
        if match and match.group(1) == "http://www.11mh.net/./":
            return True
        return False

    def getFormHash(self):
        ret = self.session.get(self.host)
        txt = ret.text
        match = re.compile(rex_formhash).search(txt)
        ret = ""
        if match:
            ret = match.group(1)
        return ret

    def doSign(self, todaySay):
        formHash = self.getFormHash()
        signUrl = self.host + "/plugin.php?id=dsu_paulsign:sign&operation=qiandao&formhash=" + formHash + "&qdmode=1&fastreply=0&qdxq=kx&infloat=yes&handlekey=dsu_paulsign&inajax=1&ajaxtarget=fwin_content_dsu_paulsign"
        data = {
            "todaysay": todaySay
        }
        ret = self.session.post(signUrl, data)

        return self.filterSignInfo(ret.text)

    def filterSignInfo(self, txt):
        match = re.compile(rex_sign).search(txt)
        if match:
            return match.group(1)
        return ""

    def loginAndSign(self, todaysay='说"签到睡觉"的是SB'):
        if self.doLogin():
            return self.doSign(todaysay)
        return "账号密码错误?"


if __name__ == '__main__':
    user = User11(USERNAME, PASSWORD)
    print(user.loginAndSign(TODAYSAY))
