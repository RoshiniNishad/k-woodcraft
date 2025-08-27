from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from difflib import SequenceMatcher
import json

# 📌 Expanded Knowledge base (FAQs)
FAQS = {
    "what are your delivery timelines": "We usually deliver within 7–14 days depending on customization and location.",
    "do you ship outside india": "Currently we serve only within India.",
    "what woods do you use": "We use teak, sheesham, acacia, and oak. Each product specifies the wood type.",
    "how do i track my order": "You will receive updates by email/phone. You can also contact support via chat.",
    "do you accept custom orders": "Yes! Share your idea/specs and we’ll craft it for you.",
    "do you offer warranty": "Yes, all our furniture comes with a 1-year warranty 🛡️.",
    "what payment modes are available": "We accept UPI, Net Banking, Cards, and Cash on Delivery (in select cities).",
    "do you provide installation": "Yes 🛠️, free installation is provided for beds, cupboards, and dining tables.",
    "do you have discounts": "🎉 Current Offer: Get 10% OFF on sofa sets and free delivery on orders above ₹20,000.",
    "can i return a product": "Yes, returns are accepted within 7 days of delivery if the item is unused and in original condition.",
    "what are your store timings": "Our physical store is open 10 AM – 8 PM, Monday to Sunday.",
    "where is your showroom located": "Our showroom is in Lucknow, Uttar Pradesh. Full address is available on the Contact page.",
    "do you provide emi options": "Yes, EMI is available via credit card and select partners.",
    "do you have free delivery": "Free delivery on all orders above ₹20,000 🚚.",
    "ok": "Great! 😊 If you have any questions, just ask.",
    "how can i contact support": "You can call 📞6394005588 or email ✉️ support@kwoodcraft.com."
}

# 📌 Expanded Keywords
KEYWORDS = {
    # Greetings & small talk
    "hi": "Hello 👋 Welcome to K-WoodCraft. How can I help you?",
    "hello": "Hi there! 😊 Ask me about delivery, payment, or furniture details.",
    "thanks": "You're welcome! 💚 Glad to help.",
    "bye": "Goodbye 👋 Have a great day!",
    "good morning": "Good morning 🌞 How can I help you today?",
    "good night": "Good night 🌙 Sweet dreams!",

    # Furniture items
    "sofa": "Our sofa sets start from ₹15,000. Available in wooden, fabric, and leather.",
    "bed": "Beds start from ₹12,000. We have King, Queen, and Single sizes.",
    "dining": "Dining tables start from ₹18,000 🍽️. Options: 4-seater & 6-seater.",
    "chair": "Wooden chairs start from ₹2,500 each.",
    "cupboard": "Cupboards/wardrobes start from ₹14,000.",
    "study table": "Study tables start from ₹6,500. Perfect for WFH & students.",
    "tv unit": "TV units start from ₹7,500. Wall-mounted & floor-standing options.",
    "bookshelf": "Bookshelves start from ₹5,000 📚. Available in teak and engineered wood.",
    "shoe rack": "Shoe racks start from ₹3,000 👟. Available in multiple sizes.",
    "office chair": "Office chairs start from ₹4,500 with ergonomic designs.",

    # Services
    "delivery": "We usually deliver within 7–14 days depending on customization and location.",
    "installation": "Yes, free installation is provided for big furniture items.",
    "return": "Returns are accepted within 7 days of delivery if unused.",
    "warranty": "All our furniture comes with a 1-year warranty 🛡️.",
    "emi": "Yes, EMI is available for easy payments.",
    "discount": "🎉 Current Offer: Get 10% OFF on sofa sets + free delivery above ₹20,000."
}

def best_answer(user_text: str) -> str:
    text = (user_text or "").lower().strip()
    if not text:
        return "Hi! How can I help you today?"

    # 1. Keyword check (fast match)
    for key, ans in KEYWORDS.items():
        if key in text:
            return ans

    # 2. Fuzzy matching with FAQs
    best_q, best_score = None, 0.0
    for q in FAQS.keys():
        score = SequenceMatcher(None, text, q).ratio()
        if score > best_score:
            best_q, best_score = q, score
    if best_score > 0.45:
        return FAQS[best_q]

    # 3. Fallback
    return "🤔 Sorry, I’m not sure. Can you share your phone/email so our team can assist you directly?"

@require_POST
@csrf_exempt
def chat_api(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = {}
    user_text = data.get("message", "")
    return JsonResponse({"reply": best_answer(user_text)})
