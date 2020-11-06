PDF = [     1,     6,    21,    56,   126,   252,   462,   792,  1287,
          2002,  2997,  4332,  6062,  8232, 10872, 13992, 17577, 21582,
         25927, 30492, 35127, 39662, 43917, 47712, 50877, 53262, 54747,
         55252, 54747, 53262, 50877, 47712, 43917, 39662, 35127, 30492,
         25927, 21582, 17577, 13992, 10872,  8232,  6062,  4332,  2997,
          2002,  1287,   792,   462,   252,   126,    56,    21,     6,
             1]

CDF = [     1,       7,      28,      84,     210,     462,     924,
          1716,    3003,    5005,    8002,   12334,   18396,   26628,
         37500,   51492,   69069,   90651,  116578,  147070,  182197,
        221859,  265776,  313488,  364365,  417627,  472374,  527626,
        582373,  635635,  686512,  734224,  778141,  817803,  852930,
        883422,  909349,  930931,  948508,  962500,  973372,  981604,
        987666,  991998,  994995,  996997,  998284,  999076,  999538,
        999790,  999916,  999972,  999993,  999999, 1000000]


# 경쟁률이 [3.5 대 1] 이면 rate = 3.5
def predict_debug(rate):
    print(f'rate={rate}')
    if rate < 1.0:
        rate = 1.0
    percentile = (1.0 - (1.0 / rate))
    rank = percentile * CDF[-1]
    print(f'rate={rate}, percentile={percentile}, rank={rank}')
    n = len(CDF)
    for idx in range(n):
        if rank <= CDF[idx]:
            print(f'percentile={percentile}, CDF[idx]={CDF[idx]}, idx={idx}')
            return idx


# 경쟁률이 [3.5 대 1] 이면 rate = 3.5
def predict(rate):
    if rate < 1.0:
        rate = 1.0
    percentile = (1.0 - (1.0 / rate)) * CDF[-1]
    n = len(CDF)
    for idx in range(n):
        if percentile < CDF[idx]:
            return idx
    return n - 1


# 참고
# 경쟁률 [백만 : 1] 결과가 54가 아니라 53이 나와도 된다면 다음처럼 등호 사용
# 대신 float-max 값 처리 가능
def predict_old(rate):
    if rate < 1.0:
        rate = 1.0
    percentile = (1.0 - (1.0 / rate)) * CDF[-1]
    for idx in range(len(CDF)):
        if percentile <= CDF[idx]:
            return idx


# 몇몇 특이값으로 테스트
def _test():
    max_num = len(CDF) - 1  # 54

    import sys

    pred = predict(-sys.float_info.max)
    assert pred == 0

    pred = predict(0.0)
    assert pred == 0

    pred = predict(1 / 1e6)
    assert pred == 0

    pred = predict(1.0)
    assert pred == 0

    pred = predict(2.0)
    assert pred == max_num * 0.5  # 27

    pred = predict(1e6)
    assert pred == max_num

    pred = predict(sys.float_info.max)
    assert pred == max_num


if __name__ == '__main__':
    _test()
