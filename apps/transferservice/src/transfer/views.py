from flask import (
    current_app,
    request, 
    jsonify,
    redirect,
)

import urllib.parse as parse
import hashlib
import base62

from src import cache
from src.libs.resp import Resp, RespCode
from .models import TransferKey
from . import transfer_bp

# @cache.cached(timeout=60 * 60 * 12, key_prefix="generated_key")
def generate_search_key(url):
    return base62.encodebytes(hashlib.md5(url.encode()).digest()[-5:])

@transfer_bp.route("/shorten", methods=["POST"])
def shorten():
    try:
        data = request.json
        url = data['targetUrl']

        if (len(url) > current_app.config["MAX_URL_LEN"]): 
            limit = current_app.config["MAX_URL_LEN"]
            raise Exception(f"URL length is longer than {limit} characters")

        parsed_url = parse.urlparse(url)
        if parsed_url.scheme not in ('http', 'https', 'ftp'):
            raise Exception(f"Missing protocols (http, https, or ftp)")

        search_key = generate_search_key(url)
        current_app.logger.info(f"Generate key: {search_key}")
        if TransferKey.check_collision(search_key, url):
            current_app.logger.info(f"Key collide")
            res = TransferKey.del_key(search_key)
            if not res: raise Exception(f"Delete failed -- {search_key}")

        current_app.logger.info(f"Set key to the db")
        res = TransferKey.set_key(search_key, url)
        if not res: raise Exception(f"Set failed -- {search_key}")
        
        return jsonify(**Resp(RespCode.SUCCESS, result={"key": search_key}).dict()), RespCode.SUCCESS

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(**Resp(RespCode.FAIL, msg=str(e)).dict()), RespCode.FAIL        


@transfer_bp.route("/redirect/<string:req_key>", methods=["GET"])
def page_redirect(req_key):
    try:
        res = TransferKey.get_key(req_key)
        if res is None: raise Exception("Key not found")
        target = res.target
        TransferKey.update_key(req_key)
        current_app.logger.info(f"Redirect -- {req_key} -- {target}")
        return redirect(target)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(**Resp(RespCode.FAIL, msg=str(e)).dict()), RespCode.FAIL