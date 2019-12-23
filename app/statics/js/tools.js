function sub_byte_string(str, max) {
    var i, res, char_bytes, length = 0, str_length = 0;
    for (i = 0; i < str.length; i++) {
        char_bytes = str.charCodeAt(i) > 127 ? 2 : 1;
        length += char_bytes;
        if (length > max) {
            break;
        }
    }
    if (i < str.length) {
        var j, omission = '...';
        var temp_length = length - (str.charCodeAt(i) > 127 ? 2 : 1);
        if (temp_length < 6) {
            return str.substring(0, i);
        }
        for (j = i; j > 0; j--) {
            temp_length -= (str.charCodeAt(j - 1) > 127 ? 2 : 1);
            if (temp_length <= max - omission.length) {
                res = str.substring(0, j - 1) + omission;
                break;
            }
        }
        return res
    }
    return str;
}