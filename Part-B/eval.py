import re

# 10 test prompts (customer messages)
test_prompts = [
    "Sir main kal EMI payment karunga",
    "Mujhe thoda time chahiye payment ke liye",
    "Next week tak payment kar dunga",
    "Aaj payment nahi kar paunga",
    "Thoda extension mil sakta hai kya",
    "Meri salary delay ho gayi hai",
    "Main next month payment kar sakta hoon",
    "Abhi paisa arrange nahi hua",
    "Please mujhe ek aur week de dijiye",
    "Payment ke liye thoda waqt chahiye"
]

# Example generated responses
# (Replace these with responses from your notebook if you want)
responses = [
    "Theek hai sir, kripya kal EMI payment complete kar dijiye.",
    "Samajh gaya sir, lekin EMI payment jaldi karna zaroori hai.",
    "Kripya next week tak payment clear kar dijiye.",
    "Theek hai sir, lekin EMI delay mat kijiye.",
    "Agar possible ho to jaldi EMI payment karein.",
    "Samajh gaya sir, lekin EMI payment pending hai.",
    "Kripya payment date confirm kar dijiye.",
    "Sir EMI payment jaldi clear karna zaroori hai.",
    "Aap extension le sakte hain, lekin payment zaroor karein.",
    "Kripya payment ka plan bata dijiye."
]

# Check if response mentions EMI/payment
def check_payment_keywords(text):
    keywords = ["emi", "payment", "pay"]
    return any(k in text.lower() for k in keywords)

# Check if response length is reasonable
def check_length(text):
    return 5 <= len(text.split()) <= 50

# Simple Hinglish/Hindi heuristic
def check_language(text):
    hinglish_words = ["hai", "sir", "kripya", "aap", "payment"]
    return any(word in text.lower() for word in hinglish_words)

def evaluate():

    total = len(responses)
    score = 0

    for i in range(total):

        payment = check_payment_keywords(responses[i])
        length = check_length(responses[i])
        language = check_language(responses[i])

        passed = payment and length and language

        if passed:
            score += 1

        print(f"Prompt {i+1}")
        print("Customer:", test_prompts[i])
        print("Agent:", responses[i])
        print("PASS" if passed else "FAIL")
        print("-" * 40)

    print(f"\nFinal Score: {score}/{total}")


if __name__ == "__main__":
    evaluate()