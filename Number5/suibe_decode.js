
const _p1 = 'NeM7Jlflm79r3LJ2'
const iv0 ='xCSwKDxsm7QxxeZC'
const pwd = 'Sgl197683!'
const CryptoJS = require('crypto-js')


var $_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
var _chars_len = $_chars.length;
function _rds(len) {
    var retStr = '';
    for (i = 0; i < len; i++) {
        retStr += $_chars.charAt(Math.floor(Math.random() * _chars_len));
    }
    return retStr;
}

function _etd2(_p0, _p1) {
        var _p2 = encryptAES(_p0, _p1);
        return _p2
}
function encryptAES(data, _p1) {
    if (!_p1) {
        return data;
    }
    var encrypted = _gas(_rds(64) + data, _p1, _rds(16));
    return encrypted;
}
function _gas(data, key0, iv0) {
    key0 = key0.replace(/(^\s+)|(\s+$)/g, "");
    var key = CryptoJS.enc.Utf8.parse(key0);
    var iv = CryptoJS.enc.Utf8.parse(iv0);
    var encrypted = CryptoJS.AES.encrypt(data, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}
const process_pwd = encryptAES(pwd,_p1)
console.log(process_pwd);
// first = _etd2()