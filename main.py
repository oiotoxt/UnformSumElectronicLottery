import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

@st.cache
def create_probability_table(n):
    # n : [각 숫자 최대값] + 1
    # st.write(n)

    # pool = np.arange(n, dtype=np.int)
    # st.write(f'pool={pool}')  # [0 1 2 3 4 5 6 7 8 9]

    array_len = ((n - 1) * 6) + 1
    X = np.arange(array_len, dtype=np.int)  # Xi는 i 번째 이벤트에서 발생한 여섯 숫자의 합
    # st.write(f'X={X}')

    P = np.zeros(array_len, dtype=np.int)  # 각 숫자합(= index)이 발생한 횟수를 여기에 저장
    C = np.zeros(array_len, dtype=np.int)  # 각 숫자합(= index)이 발생한 횟수를 여기에 저장(Cumulative)

    for i0 in range(n):
        for i1 in range(n):
            for i2 in range(n):
                for i3 in range(n):
                    for i4 in range(n):
                        for i5 in range(n):
                            P[i0 + i1 + i2 + i3 + i4 + i5] += 1

    n_event = np.sum(P)
    # st.write(f'n_event={n_event}')  # n ** 6
    # st.write(f'P={P}')

    normalized_P = P / n_event  # normalize
    # st.write(f'P[27]={P[27]}')  # 55252
    # st.write(f'(normalized_P)[27]={normalized_P[27]}')  # 0.055252

    max_P = np.max(normalized_P)

    for i in range(len(P)):
        C[i] = C[i-1] + P[i]

    # st.write(f'C={C}')
    # C=[ 1 7 28 84 210 462 924 1716 3003 5005 8002 12334 18396 26628 37500 51492 69069 90651 116578 147070 182197 221859 265776 313488 364365 417627 472374 527626 582373 635635 686512 734224 778141 817803 852930 883422 909349 930931 948508 962500 973372 981604 987666 991998 994995 996997 998284 999076 999538 999790 999916 999972 999993 999999 1000000]

    # st.write(f'C/n_event={C/n_event}')
    # C/n_event=[1.00000e-06 7.00000e-06 2.80000e-05 8.40000e-05 2.10000e-04 4.62000e-04 9.24000e-04 1.71600e-03 3.00300e-03 5.00500e-03 8.00200e-03 1.23340e-02 1.83960e-02 2.66280e-02 3.75000e-02 5.14920e-02 6.90690e-02 9.06510e-02 1.16578e-01 1.47070e-01 1.82197e-01 2.21859e-01 2.65776e-01 3.13488e-01 3.64365e-01 4.17627e-01 4.72374e-01 5.27626e-01 5.82373e-01 6.35635e-01 6.86512e-01 7.34224e-01 7.78141e-01 8.17803e-01 8.52930e-01 8.83422e-01 9.09349e-01 9.30931e-01 9.48508e-01 9.62500e-01 9.73372e-01 9.81604e-01 9.87666e-01 9.91998e-01 9.94995e-01 9.96997e-01 9.98284e-01 9.99076e-01 9.99538e-01 9.99790e-01 9.99916e-01 9.99972e-01 9.99993e-01 9.99999e-01 1.00000e+00]

    # for i in range(len(C)):
    #     if i == 0:
    #         st.write(f'{i:>2}\t0.0\t{C[i]/n_event}')
    #     else:
    #         st.write(f'{i:>2}\t{C[i-1]/n_event}\t{C[i]/n_event}')

    return array_len, n_event, P, normalized_P, max_P, C


def get_probable_num(percentile, n_event, C):
    if percentile < 0:
        return 0
    if percentile >= 1:
        return len(C) - 1

    for i in range(len(C)):
        if percentile <= C[i] / n_event:
            return i
    raise Exception('hmm')


def run():
    # st.title("Uniform-Sum Electronic Lottery - 6 Nums")
    st.markdown(
        '''## 당첨 숫자 예측
        경쟁률이 [3.5 : 1] 이라면 아래 슬라이드에서 3.5를 선택해 주세요.
        ''')

    # n : [각 숫자 최대값] + 1
    # n = st.slider("각 숫자 최대값", value=9, min_value=1, max_value=11, step=1) + 1  # 임시로 주석 처리
    n = 10

    dft_r = 2.0

    mode_option = ('Slider', 'Text')
    input_mode = st.radio('입력 방식 선택', mode_option, index=0)

    if input_mode == mode_option[0]:
        r = st.slider(
            "경쟁률", value=dft_r,
            min_value=1.0,
            max_value=10.0,
            step=0.05
        )
    elif input_mode == mode_option[1]:
        # r = st.number_input("경쟁률", min_value=1.0, max_value=None, value=dft_r)  # streamlit bug : https://github.com/streamlit/streamlit/issues/657
        # st.write(type(r))
        str_rate = st.text_input("경쟁률", value=dft_r)
        r = float(str_rate)
    else:
        raise Exception('읭?')

    if r < 1.0:
        r = 1.0

    # 확률 분포 계산
    array_len, n_event, P, normalized_P, max_P, C = create_probability_table(n)

    # 백분위 경쟁률
    percentile = 1.0 - (1.0 / r)
    st.text(f'Target percentile : {percentile * 100.0}+')

    # 필요한 숫자 합 계산
    v = get_probable_num(percentile, n_event, C)
    # st.markdown(f'### Maybe you need **{v}** or more.')
    st.markdown(f'### 당첨되려면 아마도 **{v}** 이상이 필요할거에요~')

    #
    # plot
    #

    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(1, 1, 1)

    ax.grid(True, axis='x')
    ax.set_xticks(np.arange(0, array_len, 2))
    ax.set_ylim([0.0, max_P * 1.2])

    # 분포
    x1 = np.arange(0, array_len, 1, dtype=np.int)
    ax.plot(x1, normalized_P, 'r')

    # 영역 (색칠)
    x2 = np.asarray([v, v+1], dtype=np.int)
    ax.fill_between(x2-0.5, normalized_P[v:v+1], 0, alpha=0.3, color='b')

    # 세로 라인
    ax.axvline(x=v,label='min = {}'.format(v))

    # 영역 (숫자)
    ax.text(v, normalized_P[v] * 0.33, '{:02.2f}%~{:02.2f}%'.format(C[v-1] / n_event * 100.0 if v > 0 else 0.0, C[v] / n_event * 100.0), bbox=dict(facecolor='yellow', alpha=0.5))

    ax.legend()
    st.pyplot(fig)

run()
