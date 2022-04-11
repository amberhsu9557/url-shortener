from flask import (
    current_app,
    jsonify,
)

from src.libs.resp import Resp, RespCode
from . import transfer_bp


@transfer_bp.route('/test',methods=['GET'])
def transfer_test():
    try:
        return jsonify(**Resp(RespCode.SUCCESS, msg="Transfer test OK").dict()), RespCode.SUCCESS
    except Exception as e:
        current_app.logger.warning(e,exc_info=True)
        return jsonify(**Resp(RespCode.FAIL, msg="Transfer test FAILED").dict()), RespCode.FAIL