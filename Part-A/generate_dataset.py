"""
generate_dataset.py

This script generates a synthetic dataset of 100 EMI collection call conversations
in Hindi, Hinglish, and English. Approximately 30-40% of the conversations contain
intentional data quality issues such as empty turns, duplicate turns, language
mismatches, invalid metadata, and garbled text.

The output dataset is saved as raw_conversations.jsonl and is used as the input
for the data cleaning pipeline.
"""

import json
import random
from pathlib import Path


LANGUAGES = ("hindi", "hinglish", "english")
OUTCOMES = (
    "payment_committed",
    "callback_scheduled",
    "escalated",
    "no_resolution",
)

HINDI_SCENARIOS = [
    {
        "outcome": "payment_committed",
        "turns": [
            ("agent", "नमस्ते, मैं एबीसी फाइनेंस से बोल रहा हूं। आपकी इस महीने की ईएमआई बकाया है।"),
            ("customer", "हाँ, मुझे पता है। इस बार सैलरी थोड़ी लेट आई है।"),
            ("agent", "कोई बात नहीं। क्या आप आज शाम तक भुगतान कर पाएंगे?"),
            ("customer", "जी, मैं आज शाम तक पेमेंट कर दूंगा।"),
        ],
    },
    {
        "outcome": "callback_scheduled",
        "turns": [
            ("agent", "नमस्ते, आपकी ईएमआई तीन दिन से ओवरड्यू है।"),
            ("customer", "मैं अभी मीटिंग में हूँ, क्या आप शाम को कॉल कर सकते हैं?"),
            ("agent", "ज़रूर, किस समय कॉल करना ठीक रहेगा?"),
            ("customer", "शाम 7 बजे के बाद कॉल कर लीजिए।"),
        ],
    },
    {
        "outcome": "escalated",
        "turns": [
            ("agent", "सर, आपकी लगातार दो ईएमआई पेंडिंग हैं।"),
            ("customer", "मैंने पिछले हफ्ते भुगतान किया था, फिर भी कॉल क्यों आ रही है?"),
            ("agent", "मैं सिस्टम चेक कर रहा हूं, क्या आप ट्रांजैक्शन की जानकारी साझा कर सकते हैं?"),
            ("customer", "ठीक है, लेकिन पहले किसी सीनियर से बात करवाइए।"),
        ],
    },
    {
        "outcome": "no_resolution",
        "turns": [
            ("agent", "नमस्ते, आपकी बकाया ईएमआई के बारे में बात करनी थी।"),
            ("customer", "अभी मैं यात्रा में हूँ और बात नहीं कर सकता।"),
            ("agent", "क्या कल तक भुगतान की कोई संभावना है?"),
            ("customer", "अभी कुछ कह नहीं सकता। बाद में बात करते हैं।"),
        ],
    },
]

HINGLISH_SCENARIOS = [
    {
        "outcome": "payment_committed",
        "turns": [
            ("agent", "Hello sir, aapki EMI due hai aur aaj last date hai."),
            ("customer", "Haan, mujhe yaad hai. Main office se nikalte hi payment kar dunga."),
            ("agent", "Great, payment ho jaaye to receipt save kar lijiye."),
            ("customer", "Sure, main UPI se kar deta hoon."),
        ],
    },
    {
        "outcome": "callback_scheduled",
        "turns": [
            ("agent", "Namaste ma'am, aapka installment overdue dikh raha hai."),
            ("customer", "Abhi main market mein hoon, thodi der baad call kar lo."),
            ("agent", "Theek hai, kis time pe callback set kar doon?"),
            ("customer", "Kal subah 10 baje kar lena."),
        ],
    },
    {
        "outcome": "escalated",
        "turns": [
            ("agent", "Sir, system mein do pending EMI show ho rahi hain."),
            ("customer", "Maine support ko already mail kiya tha, issue abhi tak solve nahi hua."),
            ("agent", "Main complaint note kar deta hoon aur senior team ko escalate kar deta hoon."),
            ("customer", "Please jaldi karna, warna penalty unfair lagegi."),
        ],
    },
    {
        "outcome": "no_resolution",
        "turns": [
            ("agent", "Aapka EMI account overdue hai, payment kab tak possible hoga?"),
            ("customer", "Is month thoda cash flow issue hai, exact date nahi bol sakta."),
            ("agent", "Kya partial payment possible hai?"),
            ("customer", "Nahi, abhi possible nahi hai."),
        ],
    },
]

ENGLISH_SCENARIOS = [
    {
        "outcome": "payment_committed",
        "turns": [
            ("agent", "Hello, this is a reminder that your EMI is due today."),
            ("customer", "Thanks for the reminder. I will make the payment by evening."),
            ("agent", "Please use the payment link shared on SMS after this call."),
            ("customer", "Understood, I will complete it today."),
        ],
    },
    {
        "outcome": "callback_scheduled",
        "turns": [
            ("agent", "Good afternoon, I am calling about your overdue installment."),
            ("customer", "I am driving right now. Can you call me back later tonight?"),
            ("agent", "Sure, I can arrange a callback. What time works for you?"),
            ("customer", "Please call after 8 PM."),
        ],
    },
    {
        "outcome": "escalated",
        "turns": [
            ("agent", "Our records show an unpaid EMI for your account."),
            ("customer", "I already paid and I have the receipt. This needs to be reviewed."),
            ("agent", "I will escalate this to the billing team for verification."),
            ("customer", "Please do that and update me as soon as possible."),
        ],
    },
    {
        "outcome": "no_resolution",
        "turns": [
            ("agent", "I am calling to discuss the overdue EMI on your loan account."),
            ("customer", "I am not in a position to commit to a payment date right now."),
            ("agent", "Could you share an approximate timeline for repayment?"),
            ("customer", "Not at the moment. I need a few more days to assess."),
        ],
    },
]


def clone_turns(turns):
    return [{"role": role, "text": text} for role, text in turns]


def scenario_pool(language):
    if language == "hindi":
        return HINDI_SCENARIOS
    if language == "hinglish":
        return HINGLISH_SCENARIOS
    return ENGLISH_SCENARIOS


def build_clean_conversation(index, rng):
    language = LANGUAGES[index % len(LANGUAGES)]
    scenario = rng.choice(scenario_pool(language))
    turns = clone_turns(scenario["turns"])

    if rng.random() < 0.45:
        turns.insert(
            2,
            {
                "role": "agent",
                "text": rng.choice(
                    [
                        "Please confirm if you received the payment reminder message.",
                        "कृपया बताइए कि आपको भुगतान रिमाइंडर मिला था या नहीं।",
                        "Aapko payment reminder SMS mila tha kya?",
                    ]
                ),
            },
        )
    if rng.random() < 0.25:
        turns.append(
            {
                "role": "agent",
                "text": rng.choice(
                    [
                        "Thank you for your time.",
                        "धन्यवाद, आपका दिन शुभ हो।",
                        "Thanks, main note kar deta hoon.",
                    ]
                ),
            }
        )

    return {
        "conversation_id": f"conv_{index + 1:03d}",
        "language": language,
        "turns": turns,
        "metadata": {
            "call_duration_seconds": rng.randint(75, 420),
            "outcome": scenario["outcome"],
        },
    }


def inject_empty_turns(conversation, rng):
    insertion_index = min(len(conversation["turns"]) - 1, 1)
    conversation["turns"].insert(
        insertion_index,
        {"role": rng.choice(["agent", "customer"]), "text": rng.choice(["", "   ", "\t  "])}
    )


def inject_duplicate_turn(conversation, rng):
    turn_index = rng.randrange(len(conversation["turns"]))
    duplicate_turn = dict(conversation["turns"][turn_index])
    conversation["turns"].insert(turn_index + 1, duplicate_turn)


def inject_too_few_turns(conversation, rng):
    keep_count = rng.choice([0, 1])
    conversation["turns"] = conversation["turns"][:keep_count]


def inject_invalid_metadata(conversation, rng):
    variant = rng.choice(["null_outcome", "negative_duration", "missing_metadata", "invalid_outcome"])
    if variant == "missing_metadata":
        conversation["metadata"] = {}
    elif variant == "null_outcome":
        conversation["metadata"]["outcome"] = None
    elif variant == "negative_duration":
        conversation["metadata"]["call_duration_seconds"] = -rng.randint(30, 180)
    else:
        conversation["metadata"]["outcome"] = "payment_promised_later"


def inject_language_mismatch(conversation, rng):
    replacement_language = rng.choice([lang for lang in LANGUAGES if lang != conversation["language"]])
    replacement = rng.choice(scenario_pool(replacement_language))
    conversation["turns"] = clone_turns(replacement["turns"])


def inject_garbled_text(conversation, rng):
    samples = ["PÃ¥yment ho gaya kya?", "EMI due ï»¿today", "???? ???", "kripya jaldi paymênt karein"]
    turn_index = rng.randrange(len(conversation["turns"]))
    conversation["turns"][turn_index]["text"] = rng.choice(samples)


ISSUE_HANDLERS = {
    "empty_or_whitespace_turn": inject_empty_turns,
    "duplicate_consecutive_turn": inject_duplicate_turn,
    "fewer_than_two_turns": inject_too_few_turns,
    "invalid_metadata": inject_invalid_metadata,
    "language_mismatch": inject_language_mismatch,
    "garbled_text": inject_garbled_text,
}


def apply_issues(conversation, issues, rng):
    for issue in issues:
        ISSUE_HANDLERS[issue](conversation, rng)
    conversation["synthetic_issues"] = issues
    return conversation


def corruption_plan(rng):
    issue_cycle = [
        "empty_or_whitespace_turn",
        "duplicate_consecutive_turn",
        "fewer_than_two_turns",
        "invalid_metadata",
        "language_mismatch",
        "garbled_text",
    ]
    plan = {}
    corrupted_indices = rng.sample(range(100), 35)
    for offset, index in enumerate(corrupted_indices):
        issues = [issue_cycle[offset % len(issue_cycle)]]
        if offset % 5 == 0:
            extra_candidates = [item for item in issue_cycle if item not in issues]
            issues.append(rng.choice(extra_candidates))
        plan[index] = issues
    return plan


def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    rng = random.Random(42)
    output_path = Path(__file__).with_name("raw_conversations.jsonl")
    issue_plan = corruption_plan(rng)

    conversations = []
    for index in range(100):
        conversation = build_clean_conversation(index, rng)
        issues = issue_plan.get(index)
        if issues:
            conversation = apply_issues(conversation, issues, rng)
        conversations.append(conversation)

    write_jsonl(output_path, conversations)

    corrupted_count = sum(1 for item in conversations if item.get("synthetic_issues"))
    print(f"Wrote {len(conversations)} conversations to {output_path.name}")
    print(f"Corrupted conversations: {corrupted_count}")
    print("Language distribution:")
    for language in LANGUAGES:
        count = sum(1 for item in conversations if item["language"] == language)
        print(f"  {language}: {count}")


if __name__ == "__main__":
    main()