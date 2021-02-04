
import os
import sys
import json
import ssl

import tornado.httpserver
import tornado.ioloop
import tornado.web

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "img"))
sys.path.append(os.path.join(os.path.dirname(__file__), "js"))
from keyboard_dynamics import get_diffs, clear_diffs, add_to_diffs
from keyboard_dynamics import get_average_diffs, get_err
from keyboard_dynamics import MIN_DIFFS_LEN, MIN_NUM_ENTRIES
from keyboard_dynamics import uuid_is_allowed
from keyboard_dynamics import CUR_AVG_ERR_RATIO
from responses import uuid_not_registered, password_too_short
from responses import pattern_mismatch, pattern_matches
from responses import too_few_patterns, mismatch_msg, matches_msg


USER_UUID_ARG = "uuid"


class MainPage(tornado.web.RequestHandler):
    def get(self):
        with open("index.html") as fh:
            html = fh.read()
        self.write(html)


class CheckTimes(tornado.web.RequestHandler):
    def post(self):
        body_dict = json.loads(self.request.body)
        if not uuid_is_allowed(body_dict[USER_UUID_ARG]):
            self.set_status(400)
            self.finish(json.dumps(uuid_not_registered))
        else:
            cur_diffs = get_diffs(body_dict["times"])
            avg_diffs, avg_err, num_entries = get_average_diffs(body_dict[USER_UUID_ARG])

            if len(cur_diffs) < MIN_DIFFS_LEN:
                self.set_status(400)
                self.finish(json.dumps(password_too_short))
            elif num_entries < MIN_NUM_ENTRIES:
                if len(cur_diffs) >= MIN_DIFFS_LEN:
                    add_to_diffs(cur_diffs, body_dict[USER_UUID_ARG])
                self.write(json.dumps(too_few_patterns))
            else:
                add_to_diffs(cur_diffs, body_dict[USER_UUID_ARG])
                cur_err = get_err(avg_diffs, cur_diffs)
                cutoff_err = CUR_AVG_ERR_RATIO * avg_err
                if cur_err > cutoff_err:
                    pattern_mismatch["msg"] = mismatch_msg.format(avg_err,
                        cur_err, cutoff_err)
                    self.write(json.dumps(pattern_mismatch))
                else:
                    pattern_matches["msg"] = matches_msg.format(avg_err,
                        cur_err, cutoff_err)
                    self.write(json.dumps(pattern_matches))
                self.set_status(200)


class ClearTimes(tornado.web.RequestHandler):
    def delete(self):
        user_uuid = json.loads(self.request.body)[USER_UUID_ARG]
        if not uuid_is_allowed(user_uuid):
            self.set_status(400)
            self.finish(uuid_not_registered)

        clear_diffs(user_uuid)
        self.set_status(200)


def make_app():
    return tornado.web.Application([
        (r"/", MainPage),
        (r"/checkTimes", CheckTimes),
        (r"/clearTimes", ClearTimes),
        (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': './js'}),
        (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': './img'})
    ])


if __name__ == "__main__":
    app = make_app()

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("../../certificate/your_certificate_name_here.crt",
                            "../../certificate/your_certificate_name_here.key")
    http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
    http_server.listen(443)
    print("Listening...")
    tornado.ioloop.IOLoop.current().start()

