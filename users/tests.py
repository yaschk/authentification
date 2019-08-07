import string


allowed_chars=string.ascii_letters + string.digits + '_-.'
allowed_set = set(allowed_chars)
trans_table = string.maketrans('','')

def check_trans(s):
    return not s.translate(trans_table,allowed_chars)

strrr = ''

print(check_set_diff(strrr))