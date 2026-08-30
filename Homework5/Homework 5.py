# กำหนดค่าความน่าจะเป็นจากตารางใน image.png

# Table 1 - Prior for Smoking: P(S)
P_S = {
    True: 0.30,
    False: 0.70
}

# Table 2 - Conditional for Lung Cancer given Smoking: P(C | S)
# รูปแบบ: P_C_given_S[(C, S)]
P_C_given_S = {
    (True, True): 0.05,
    (False, True): 0.95,
    (True, False): 0.01,
    (False, False): 0.99
}

# Table 3 - Conditional for X-Ray Result given Cancer Status: P(T | C)
# รูปแบบ: P_T_given_C[(T, C)] โดยใช้ '+' แทน "บวก" และ '-' แทน "ลบ"
P_T_given_C = {
    ('+', True): 0.90,
    ('-', True): 0.10,
    ('+', False): 0.20,
    ('-', False): 0.80
}

# ---------------------------------------------------------
# ฟังก์ชันสำหรับคำนวณ Joint Probability: P(S, C, T) = P(S) * P(C|S) * P(T|C)
def joint_prob(s, c, t):
    return P_S[s] * P_C_given_S[(c, s)] * P_T_given_C[(t, c)]

print("--- ผลการคำนวณ ---")

# ข้อ 41. จงคำนวณหาค่า P(S = true, C = true, T = "บวก")
# สูตร: P(S=T) * P(C=T | S=T) * P(T='+' | C=T)
ans_41 = joint_prob(True, True, '+')
print(f"ข้อ 41: P(S=true, C=true, T='บวก') = {ans_41:.4f}") 
# ตรงกับช้อยส์ (b) 0.0135


# ข้อ 42. จงคำนวณหาโอกาสทั้งหมดที่จะให้ผลตรวจเอกซเรย์เป็นบวก: P(T = "บวก")
# สูตร: ผลรวมของ P(S, C, T="+") ในทุกๆ กรณีของ S และ C (Marginalization)
ans_42 = 0
for s in [True, False]:
    for c in [True, False]:
        ans_42 += joint_prob(s, c, '+')
print(f"ข้อ 42: P(T='บวก') = {ans_42:.4f}")
# ตรงกับช้อยส์ (b) 0.2154


# ข้อ 43. จงคำนวณหาค่า Posterior: Cancer | Positive X-Ray : P(C = true | T = "บวก")
# สูตร Bayes' Theorem: P(C=T | T="+") = P(C=T, T="+") / P(T="+")
# 1. หา P(C=true, T="บวก") ก่อน
p_c_true_and_t_pos = 0
for s in [True, False]:
    p_c_true_and_t_pos += joint_prob(s, True, '+')

# 2. นำไปหารด้วย P(T="บวก") จากข้อ 42
ans_43 = p_c_true_and_t_pos / ans_42
print(f"ข้อ 43: P(C=true | T='บวก') = {ans_43:.3f}")
# ตรงกับช้อยส์ (b) 0.092


# ข้อ 44. จงคำนวณหาค่า Posterior: Smoker | Positive X-Ray : P(S = true | T = "บวก")
# สูตร Bayes' Theorem: P(S=T | T="+") = P(S=T, T="+") / P(T="+")
# 1. หา P(S=true, T="บวก") ก่อน
p_s_true_and_t_pos = 0
for c in [True, False]:
    p_s_true_and_t_pos += joint_prob(True, c, '+')

# 2. นำไปหารด้วย P(T="บวก") จากข้อ 42
ans_44 = p_s_true_and_t_pos / ans_42
print(f"ข้อ 44: P(S=true | T='บวก') = {ans_44:.3f}")
# ตรงกับช้อยส์ (a) 0.327


# ข้อ 45. หากมีผู้ป่วย 1,000 คน ... คาดว่าจะมีผู้ที่เป็นมะเร็งและผลเอกซเรย์เป็นบวก กี่ราย?
# สูตร: Expected Value = จำนวนคน * P(C=true, T="บวก")
# เราคำนวณ P(C=true, T="บวก") ไว้แล้วในขั้นตอนของข้อ 43 (ตัวแปร p_c_true_and_t_pos)
ans_45 = 1000 * p_c_true_and_t_pos
print(f"ข้อ 45: จำนวนคนที่เป็นมะเร็งและเอกซเรย์บวก = {ans_45:.1f} คน (ประมาณ {round(ans_45)} คน)")
# ตรงกับช้อยส์ (b) ≈ 20