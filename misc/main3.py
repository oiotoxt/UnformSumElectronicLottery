C =   [      1,       7,      28,      84,     210,     462,     924,
          1716,    3003,    5005,    8002,   12334,   18396,   26628,
         37500,   51492,   69069,   90651,  116578,  147070,  182197,
        221859,  265776,  313488,  364365,  417627,  472374,  527626,
        582373,  635635,  686512,  734224,  778141,  817803,  852930,
        883422,  909349,  930931,  948508,  962500,  973372,  981604,
        987666,  991998,  994995,  996997,  998284,  999076,  999538,
        999790,  999916,  999972,  999993,  999999, 1000000]


# [3.5 대 1] 이면 rate = 3.5
def get_probable_num(rate, C):
    if rate < 1.0:
        rate = 1.0

    # 백분위 경쟁률
    percentile = 1.0 - (1.0 / rate)
    print(f'Target percentile : {percentile * 100.0}+')

    if percentile < 0:
        return 0
    if percentile >= 1:
        return len(C) - 1

    for i in range(len(C)):
        if percentile <= C[i] / 1e6:
            return i
    raise Exception('hmm')


def run(rate):
    # 필요한 숫자 합 계산
    v = get_probable_num(rate, C)
    print(f'### 당첨되려면 아마도 **{v}** 이상이 필요할거에요~')


run(2.0)
