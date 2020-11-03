import numpy as np

_CDF = [     1,       7,      28,      84,     210,     462,     924,
          1716,    3003,    5005,    8002,   12334,   18396,   26628,
         37500,   51492,   69069,   90651,  116578,  147070,  182197,
        221859,  265776,  313488,  364365,  417627,  472374,  527626,
        582373,  635635,  686512,  734224,  778141,  817803,  852930,
        883422,  909349,  930931,  948508,  962500,  973372,  981604,
        987666,  991998,  994995,  996997,  998284,  999076,  999538,
        999790,  999916,  999972,  999993,  999999, 1000000]


# 경쟁률이 [3.5 대 1] 이면 rate = 3.5
def predict(rate, CDF):
    if rate < 1.0:
        rate = 1.0

    percentile = 1.0 - (1.0 / rate)
    percentile *= CDF[-1]
    for idx in range(len(CDF)):
        if percentile <= CDF[idx]:
            return idx
    raise Exception('읭?')


def _test():
    max_num = len(_CDF) - 1  # 54

    import sys

    pred = predict(-sys.float_info.max, _CDF)
    assert pred == 0

    pred = predict(0.0, _CDF)
    assert pred == 0

    pred = predict(1.0, _CDF)
    assert pred == 0

    pred = predict(2.0, _CDF)
    assert pred == max_num * 0.5  # 27

    pred = predict(sys.float_info.max, _CDF)
    assert pred == max_num


if __name__ == '__main__':
    _test()
