
from keyboard_dynamics import MIN_DIFFS_LEN, MIN_NUM_ENTRIES


uuid_not_registered = {
    "pattern_match": False,
    "msg": "User uuid specified is not registered!"
}


password_too_short = {
    "pattern_match": False,
    "msg": "Password should be > {} characters!".format(MIN_DIFFS_LEN/2)
}


mismatch_msg = ("Keystroke pattern does Not match! "
                "Average error between past patterns: {}. "
                "Current error: {}.  Cutoff error: {}.")
pattern_mismatch = {
    "pattern_match": False,
    "msg": None
}


matches_msg = ("Keystroke pattern matches. "
               "Average error between past patterns: {}. "
               "Current error: {}.  Cutoff error: {}.")
pattern_matches = {
    "pattern_match": True,
    "msg": None
}


too_few_patterns = {
    "pattern_match": True,
    "msg": "Need {} or more password patterns.".format(MIN_NUM_ENTRIES)
}

