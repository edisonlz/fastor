#coding=utf-8
import string


class ShortID(object):
    def __init__(self):
        self.dic = string.ascii_letters + string.digits
        self.mod = len(self.dic)

    def toHex(self, oid):
        results = ""

        while oid > 0:
            index = oid % self.mod
            results += self.dic[index]
            oid = oid / self.mod
        return results

    def toID(self, ihex):
        results = 0
        position = len(ihex) - 1
        for i, val in enumerate(reversed(ihex)):

            h = self.dic.find(val)
            if h < 0:
                return -1
            results += h * self.mod ** position
            position -= 1

        return results


if __name__ == "__main__":

    sid = ShortID()

    # a = sid.toHex(1)
    # print a,sid.toID(a)
    # assert sid.toID(a) == 1

    for i in xrange(0, 1000000):
        a = sid.toHex(i)
        e = sid.toID(a)
        print i, a, e
        assert sid.toID(a) == i















