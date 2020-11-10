import numpy as np


def create_probability_table(n=10):
    '''
        랜덤한 숫자 6개 합의 PDF 및 CDF 생성

        n : 각 자리에 가능한 값 갯수. [0,9]라면 10
    '''

    array_len = ((n - 1) * 6) + 1  # (n == 10) 이면 55

    # PDF
    PDF = np.zeros(array_len, dtype=np.int)  # 각 숫자합이 발생한 횟수를 여기에 저장
    for i0 in range(n):
        for i1 in range(n):
            for i2 in range(n):
                for i3 in range(n):
                    for i4 in range(n):
                        for i5 in range(n):
                            PDF[i0 + i1 + i2 + i3 + i4 + i5] += 1

    # print(repr(PDF))
    n_event = np.sum(PDF)  # == n ** 6
    norm_PDF = PDF / n_event
    max_PDF = np.max(norm_PDF)

    # CDF
    CDF = np.zeros(array_len, dtype=np.int)  # 각 숫자합이 발생한 횟수를 누적해 가며 여기에 저장
    for i in range(len(PDF)):
        CDF[i] = CDF[i-1] + PDF[i]
    # print(repr(CDF))
    return array_len, n_event, PDF, norm_PDF, max_PDF, CDF


# 경쟁률이 [3.5 대 1] 이면 rate = 3.5
def predict(rate, CDF):
    print(f'Rate : [{rate} 대 1]')
    if rate < 1.0:
        rate = 1.0

    percentile = 1.0 - (1.0 / rate)
    print(f'Target percentile : {percentile * 100.0}+')
    percentile *= CDF[-1]
    for i in range(len(CDF)):
        if percentile <= CDF[i]:
            return i
    raise Exception('hmm')

# pre-calc
_PDF = [     1,     6,    21,    56,   126,   252,   462,   792,  1287,
          2002,  2997,  4332,  6062,  8232, 10872, 13992, 17577, 21582,
         25927, 30492, 35127, 39662, 43917, 47712, 50877, 53262, 54747,
         55252, 54747, 53262, 50877, 47712, 43917, 39662, 35127, 30492,
         25927, 21582, 17577, 13992, 10872,  8232,  6062,  4332,  2997,
          2002,  1287,   792,   462,   252,   126,    56,    21,     6,
             1]

# pre-calc
_CDF = [     1,       7,      28,      84,     210,     462,     924,
          1716,    3003,    5005,    8002,   12334,   18396,   26628,
         37500,   51492,   69069,   90651,  116578,  147070,  182197,
        221859,  265776,  313488,  364365,  417627,  472374,  527626,
        582373,  635635,  686512,  734224,  778141,  817803,  852930,
        883422,  909349,  930931,  948508,  962500,  973372,  981604,
        987666,  991998,  994995,  996997,  998284,  999076,  999538,
        999790,  999916,  999972,  999993,  999999, 1000000]


def run(rate):
    CDF = None
    use_precalc_cdf = False
    if use_precalc_cdf:
        CDF = _CDF
    else:
        _, _, _, _, _, CDF = create_probability_table(10)

    # 필요한 숫자 합 계산
    pred = predict(rate, CDF)
    print(f'당첨되려면 아마도 {pred} 이상이 필요할거에요~')


if __name__ == '__main__':
    run(2.0)
