
import os
import json
from uuid import uuid4  # uuid4().hex string


base_path = os.path.join(os.path.dirname(__file__), "../")
patterns_base_path = os.path.join(base_path, "keystroke_patterns")
NUM_PATTERNS    = 5   # number of last password patterns to store
MIN_NUM_ENTRIES = 3   # if time diffs array is shorter, don't do verification
MIN_DIFFS_LEN   = 6   # only process passwords >= 3 chars
CUR_AVG_ERR_RATIO = 1.6  # if current error is > CUR_AVG_ERR_RATIO * average error
                         # then keystrokes do Not match


def uuid_is_allowed(user_uuid):
    allowed_uuids_path = os.path.join(base_path, "allowed_uuids.json")
    with open(allowed_uuids_path, "r") as fh:
        allowed_uuids = json.load(fh)
    return user_uuid in allowed_uuids


def load_past_diffs(user_uuid):
    history_file_path = os.path.join(patterns_base_path, user_uuid)
    if not os.path.exists(history_file_path):
        past_diffs = []
        with open(history_file_path, "w") as fh:
            json.dump(past_diffs, fh)
    else:
        with open(history_file_path, "r") as fh:
            past_diffs = json.load(fh)
    return past_diffs


def get_average_diffs(user_uuid):
    """
    Return average time diffs and the average error ms per password entry,
    and the number of historical passwords entered
    """
    diffs_list = load_past_diffs(user_uuid)
    if not diffs_list:
        return [], 0, 0

    avg = []
    err_total = 0
    min_len = min(len(x) for x in diffs_list)
    num_lists = len(diffs_list)
    for idx in range(min_len):
        avg_diff = sum(x[idx] for x in diffs_list) / num_lists
        err_total += sum(abs(x[idx]-avg_diff) for x in diffs_list)
        avg.append(avg_diff)
    return avg, round(err_total/num_lists), num_lists


def get_err(avg, diffs):
    min_len = min(len(avg), len(diffs))
    err = 0
    for idx in range(min_len):
        err += abs(diffs[idx] - avg[idx])
    return round(err)


def add_to_diffs(diff, user_uuid):
    history_file_path = os.path.join(patterns_base_path, user_uuid)
    curr_diffs = load_past_diffs(user_uuid)
    if len(curr_diffs) > NUM_PATTERNS:
        curr_diffs = curr_diffs[-NUM_PATTERNS:]
    curr_diffs.append(diff)
    with open(history_file_path, "w") as fh:
        json.dump(curr_diffs, fh)


def clear_diffs(user_uuid):
    history_file_path = os.path.join(patterns_base_path, user_uuid)
    with open(history_file_path, "w") as fh:
        json.dump([], fh)


def get_diffs(times):
    diffs = []
    for idx in range(len(times)-1):
        diffs.append(abs(times[idx+1] - times[idx]))
    return diffs

