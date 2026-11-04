import os
import sys
import webbrowser
import time
import speech_recognition as sr
from gtts import gTTS
from google import genai

# ==================== VOICE / TEXT HYBRID ENGINE ====================
def speak(text):
    """अगर मोबाइल या कंप्यूटर पर साउंड सपोर्ट होगा तो बोलेगा, नहीं तो सिर्फ प्रिंट करेगा"""
    print(f"Jarvis: {text}")
    try:
        # यह मोबाइल (Android Termux/Pydroid) पर बैकग्राउंड में ऑडियो प्ले करने के लिए है
        # कंप्यूटर पर बिना साउंड बॉक्स के यह लाइन एरर नहीं देगी, सिर्फ स्किप हो जाएगी
        tts = gTTS(text=text, lang='hi')
        tts.save("reply.mp3")
        if os.name == 'posix': # मोबाइल/लिनक्स के लिए
            os.system("mpv reply.mp3 --noconsole &") 
    except Exception:
        pass # साउंड बॉक्स न होने पर कोड क्रैश नहीं होगा

def listen_voice():
    """माइक से इनपुट लेने की कोशिश करेगा, एरर आने पर टाइपिंग मोड पर आ जाएगा"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\n🎙️ सुन रहा हूँ... (बोलिए या स्क्रीन पर देखते रहिए)")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            query = r.recognize_google(audio, language='hi-IN')
            print(f"आप (आवाज़): {query}")
            return query
    except Exception:
        # अगर कंप्यूटर में माइक/साउंड इनपुट नहीं है, तो यह तुरंत टाइप करने का विकल्प दे देगा
        print("\n[सिस्टम नोट: माइक नहीं मिला। कृपया नीचे टाइप करें]")
        typed_input = input("आप (टाइप करें): ").strip()
        return typed_input

# ==================== LOGIN SYSTEM ====================
DB_FILE = "users_database.txt"
OWNER_NUMBER_RAW = "9717804643"
OWNER_NUMBER_FULL = "+919717804643"

def read_users():
    if not os.path.exists(DB_FILE): return {}
    users = {}
    with open(DB_FILE, "r") as f:
        for line in f:
            if "," in line:
                u, p = line.strip().split(",")
                users[u] = p
    return users

def run_login_system():
    while True:
        print("="*60)
        print("🤖 जार्विस हाइब्रिड लॉगिन गेटवे (PC & Mobile)")
        print("="*60)
        print("1. लॉगिन करें (Login)\n2. नया अकाउंट बनाएं (Register)\n3. ऐप बंद करें (Exit)")
        choice = input("अपना विकल्प चुनें: ").strip()
        
        if choice == "2":
            user_id = input("Mobile / Email: ").strip()
            password = input("Password: ").strip()
            if not user_id or not password: continue
            users = read_users()
            if user_id in users: print("❌ पहले से रजिस्टर्ड है!")
            else:
                with open(DB_FILE, "a") as f: f.write(f"{user_id},{password}\n")
                print("🎉 अकाउंट बन गया!")
        elif choice == "1":
            user_id = input("Registered Mobile / Email: ").strip()
            if user_id == OWNER_NUMBER_RAW or user_id == OWNER_NUMBER_FULL:
                print(f"\n✅ स्वागत है शौराव मालिक! नंबर वेरीफाई हो गया।")
                break
            password = input("Password: ").strip()
            users = read_users()
            if user_id in users and users[user_id] == password: break
            else: print("❌ गलत पासवर्ड!")
        elif choice == "3": sys.exit()

# ==================== AI CLIENT ====================
API_KEY = "AQ.Ab8RN6Jz_o6ySBvjgLiTvMlzRGNtdIcmK88j663Zp9PnHdwHxw"
try:
    client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

def get_ai_response(user_input):
    if not client: return "AI एक्टिवेट नहीं हो पाया।"
    for attempt in range(3):
        try:
            system_instruction = (
                "You are Jarvis, a smart AI assistant. Keep responses short and friendly. "
                "Reply in Hindi/Hinglish."
            )
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=user_input,
                config={'system_instruction': system_instruction}
            )
            return response.text
        except Exception:
            if attempt < 2: time.sleep(1); continue
            return "सर्वर पर लोड है, दोबारा लिखें।"

# ==================== HYBRID VOICE CALL MODE ====================
def start_voice_call_mode():
    speak("कॉल मोड सक्रिय कर दिया गया है।")
    print("📞 [LIVE CHAT ACTIVE] - बाहर निकलने के लिए 'exit' लिखें या बोलें।")
    
    while True:
        command = listen_voice()
        if not command: continue
        if "exit" in command.lower() or "कट करो" in command:
            speak("कॉल डिस्कनेक्ट हो रही है।")
            break
        
        reply = get_ai_response(command)
        speak(reply)

# ==================== MAIN ASSISTANT ====================
def jarvis_assistant():
    print("🤖 जार्विस AI 3.5 (Hybrid PC/Mobile) एक्टिवेट हो गया है...")
    
    while True:
        print("\n💡 सामान्य चैट करें या लाइव कॉल के लिए 'call jarvis' लिखें।")
        command = input("आप: ").strip()
        if not command: continue
        command_lower = command.lower()
        
        if "exit" in command_lower:
            print("Jarvis: गुडबाय मालिक!")
            sys.exit()
        elif "open youtube" in command_lower:
            webbrowser.open("https://youtube.com")
        elif "open google" in command_lower:
            webbrowser.open("https://google.com")
        elif "call jarvis" in command_lower or "start call" in command_lower:
            start_voice_call_mode()
        else:
            ai_reply = get_ai_response(command)
            print(f"Jarvis: {ai_reply}")

if __name__ == "__main__":
    run_login_system()
    jarvis_assistant()
