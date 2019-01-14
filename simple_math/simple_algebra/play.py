def score_ans(cal_answer, correct_ans):
    score = 0
    len_a = len(cal_answer)
    len_b = len(correct_ans)
    shorter_len = 0
    if len_a < len_b:
        shorter_len = len_a
    else:
        shorter_len = len_b

    for i in range(0, shorter_len):
        char_a = cal_answer[i]
        char_b = correct_ans[i]

        if char_a != char_b:
            score += shorter_len - i

    return score


a = score_ans('-233', '-12333')
print(a)