from __future__ import annotations

import json
import os
import re
from typing import Any, Dict

from app.core.llm_bridge import llm_bridge


def _normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip()


def _normalized_context(context: Dict[str, Any] | None) -> Dict[str, Any]:
    if not isinstance(context, dict):
        return {}

    allowed_keys = [
        "platform",
        "device",
        "preferred_language",
        "detected_language",
        "city",
        "location",
        "region",
        "session_id",
    ]
    normalized = {
        key: context.get(key)
        for key in allowed_keys
        if context.get(key) not in (None, "", {}, [])
    }
    return normalized


def _preferred_model(requested_model: str | None) -> str:
    requested = (requested_model or "").strip().lower()
    if requested and requested != "uniguru":
        return requested

    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("OPENAI_API_KEY"):
        return "chatgpt"
    if os.getenv("GOOGLE_API_KEY"):
        return "gemini"
    if os.getenv("MISTRAL_API_KEY"):
        return "mistral"
    return "uniguru"


def _response_language(context: Dict[str, Any] | None) -> str:
    normalized_context = _normalized_context(context)
    preferred = str(normalized_context.get("preferred_language") or "").strip().lower()
    detected = str(normalized_context.get("detected_language") or "").strip().lower()

    if preferred and preferred != "auto":
        return preferred
    if detected and detected != "auto":
        return detected
    return "en"


def _language_label(language_code: str) -> str:
    labels = {
        "en": "English",
        "hi": "Hindi",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ar": "Arabic",
    }
    return labels.get(language_code, language_code or "English")


def build_response_prompt(query: str, context: Dict[str, Any] | None = None) -> str:
    cleaned_query = _normalized_text(query)
    cleaned_context = _normalized_context(context)
    context_blob = json.dumps(cleaned_context, sort_keys=True, ensure_ascii=True)
    response_language = _response_language(cleaned_context)
    response_language_label = _language_label(response_language)

    return (
        "You are Mitra, a professional, knowledgeable, and helpful AI assistant.\n"
        "Your role is to provide accurate, comprehensive, and well-structured answers to ANY question.\n\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "CORE Capabilities:\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "- 🧮 MATHEMATICS: Solve any math problem, show formulas, step-by-step solutions\n"
        "- 🔬 SCIENCE: Physics, Chemistry, Biology, Astronomy, Earth Science\n"
        "- 💡 TECHNOLOGY: Programming, AI, ML, Computer Science, Engineering\n"
        "- 📚 EDUCATION: History, Geography, Literature, Languages\n"
        "- 🧠 PSYCHOLOGY: Human behavior, mental health, cognitive science\n"
        "- 💼 BUSINESS: Economics, Finance, Management, Marketing\n"
        "- 🏥 HEALTH: Medicine, Nutrition, Fitness, Wellness\n"
        "- 🎨 ARTS: Music, Painting, Literature, Culture\n"
        "- 🌍 GENERAL: Any topic, current events, how things work\n\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "RESPONSE FORMAT:\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        f"- Language: {response_language_label}\n"
        "- Use markdown formatting: headers (##), bold (**text**), bullet points\n"
        "- For math: Show the formula, then solve step-by-step\n"
        "- For definitions: Clear definition first, then examples\n"
        "- For explanations: Use logical sections with headings\n"
        "- For comparisons: Use tables when helpful\n"
        "- Be concise but comprehensive\n"
        "- Always provide accurate information\n"
        "- If unsure, acknowledge limitations honestly\n\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "IMPORTANT RULES:\n"
        "═══════════════════════════════════════════════════════════════════════════════\n"
        "- NEVER say 'I cannot' or 'I don't know' without trying first\n"
        "- NEVER generate fake or made-up information\n"
        "- ALWAYS provide the best answer you can based on your knowledge\n"
        "- For math problems: ALWAYS calculate and show the answer\n"
        "- For formulas: Show the formula and explain each variable\n"
        "- For scientific questions: Provide accurate, factual information\n"
        "- Do NOT repeat the user's question back\n"
        "- Do NOT mention being an AI or having limitations unless asked\n\n"
        f"Runtime context: {context_blob}\n"
        f"User question: {cleaned_query}\n\n"
        "Provide a professional, accurate, and well-formatted answer:"
    )


def build_fallback_response(query: str, context: Dict[str, Any] | None = None) -> str:
    text = _normalized_text(query)
    lower = text.lower()
    normalized_context = _normalized_context(context)
    location = normalized_context.get("city") or normalized_context.get("location") or normalized_context.get("region")
    response_language = _response_language(normalized_context)

    if response_language != "en":
        response_language = "en"

    # ===== GREETINGS =====
    if any(lower.startswith(token) or lower == token for token in ["how are you", "how're you", "how do you do"]):
        return "I'm doing well, thank you for asking! I'm Mitra, your AI assistant. How can I help you today?"
    if any(lower.startswith(token) or lower == token for token in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! I'm Mitra, your AI assistant. I can help you with questions, tasks, messaging, reminders, and more. What would you like to do?"
    if any(lower.startswith(token) or lower == token for token in ["what is your name", "what's your name", "who are you", "tell me about yourself"]):
        return (
            "# 👋 Hello! I'm Mitra\n\n"
            "## About Me\n"
            "I'm an AI assistant designed to help you with various tasks. I'm part of the BHIV ecosystem "
            "and serve as your unified interface for all BHIV products.\n\n"
            "## What I Do\n"
            "- 💬 **Communication**: Send messages across WhatsApp, Email, Telegram, and more\n"
            "- 📅 **Productivity**: Set reminders, manage calendar events, create tasks\n"
            "- 🧠 **Knowledge**: Answer questions and provide information\n"
            "- 🌐 **Multi-language**: Support for multiple languages\n"
            "- 🔗 **Integration**: Connect with BHIV ecosystem products\n\n"
            "## How to Use Me\n"
            "Just ask me anything or tell me what you need! I'm here to help.\n\n"
            "What would you like to do today?"
        )

    # ===== CAPABILITY QUESTIONS =====
    if any(token in lower for token in ["what can you do", "help me with", "how can you help", "what are your features", "capabilities"]):
        return (
            "# 🤖 Mitra - Your AI Assistant\n\n"
            "## What I Can Do\n\n"
            "### 💬 Communication\n"
            "- Send emails, WhatsApp messages, and Telegram messages\n"
            "- Multi-language support\n"
            "- Voice input/output\n\n"
            "### 📅 Productivity\n"
            "- Set reminders and manage calendar events\n"
            "- Create and assign tasks\n"
            "- Schedule meetings\n\n"
            "### 🧠 Knowledge\n"
            "- Answer questions on various topics\n"
            "- Explain concepts and ideas\n"
            "- Provide information and insights\n\n"
            "### 🔧 Integration\n"
            "- Connect with BHIV ecosystem products\n"
            "- Execute actions across platforms\n"
            "- Unified execution gateway\n\n"
            "### 🛡️ Safety\n"
            "- Content moderation\n"
            "- Privacy protection\n"
            "- Secure authentication\n\n"
            "Just ask me anything or tell me what you need!"
        )

    # ===== MATH CALCULATIONS (MUST BE FIRST) =====
    import re
    
    # Helper function to safely evaluate math expressions
    def safe_eval(expr):
        """Safely evaluate a math expression."""
        # Remove any non-math characters except numbers, operators, parentheses, spaces, dots
        cleaned = re.sub(r'[^0-9\+\-\*\/\%\.\(\)\s]', '', expr)
        if not cleaned:
            return None
        try:
            # Only allow math operations
            result = eval(cleaned, {"__builtins__": {}}, {})
            return result
        except:
            return None
    
    # Convert word operators to symbols
    def convert_word_operators(text):
        """Convert word-based operators to symbols."""
        text = re.sub(r'\bplus\b', '+', text)
        text = re.sub(r'\bminus\b', '-', text)
        text = re.sub(r'\btimes\b', '*', text)
        text = re.sub(r'\bmultiplied by\b', '*', text)
        text = re.sub(r'\bdivided by\b', '/', text)
        text = re.sub(r'\bover\b', '/', text)
        text = re.sub(r'\bmod\b', '%', text)
        text = re.sub(r'\bmodulo\b', '%', text)
        return text
    
    # Check for explicit math keywords first
    math_keywords = ["calculate", "math", "compute", "what's", "solve", "evaluate"]
    is_math_query = any(token in lower for token in math_keywords)
    
    # Convert word operators in the original text
    converted_text = convert_word_operators(text.lower())
    
    # Check for math expressions with operators (including parentheses)
    # Matches: 2+2, 2+2+2, 10-5, 3*4, 10/2, 10%3, (2+3)*4, etc.
    # More permissive regex that allows parentheses at start/end
    math_expression = re.search(r'([\d\(\)][\d\s\+\-\*\/\%\.\(\)]*[\d\)])', converted_text)
    
    # Check for "what is" followed by math
    what_is_math = re.search(r'what is\s+([\d\(\)][\d\s\+\-\*\/\%\.\(\)]*[\d\)])', converted_text)
    what_s_math = re.search(r"what's\s+([\d\(\)][\d\s\+\-\*\/\%\.\(\)]*[\d\)])", converted_text)
    
    if is_math_query or math_expression or what_is_math or what_s_math:
        # Try to extract the math expression
        expr = None
        if what_is_math:
            expr = what_is_math.group(1)
        elif what_s_math:
            expr = what_s_math.group(1)
        elif math_expression:
            expr = math_expression.group(1)
        
        if expr:
            result = safe_eval(expr)
            if result is not None:
                # Format the result nicely
                if isinstance(result, float) and result == int(result):
                    result = int(result)
                return (
                    f"# 🧮 Calculation Result\n\n"
                    f"**Expression:** `{expr}`\n\n"
                    f"**Answer:** `{result}`\n\n"
                    f"Would you like me to help with anything else?"
                )
    
    # ===== KNOWLEDGE QUESTIONS =====
    if "what is" in lower or "what are" in lower or "tell me about" in lower or "explain me about" in lower or "explain about" in lower:
        # Extract the topic
        topic = ""
        for prefix in ["what is ", "what are ", "tell me about ", "explain me about ", "explain about "]:
            if prefix in lower:
                topic = text[lower.index(prefix) + len(prefix):].strip()
                break
        
        if topic:
            # Provide informative responses for common topics
            topic_lower = topic.lower()
            
            if any(t in topic_lower for t in ["reinforcement learning", "rl", "machine learning"]):
                return (
                    "# 🎯 Reinforcement Learning (RL)\n\n"
                    "## Definition\n"
                    "Reinforcement Learning is a type of machine learning where an agent learns to make decisions "
                    "by taking actions in an environment to maximize cumulative rewards.\n\n"
                    "## Key Concepts\n"
                    "| Concept | Description |\n"
                    "|---------|-------------|\n"
                    "| **Agent** | The learner/decision-maker |\n"
                    "| **Environment** | The world the agent interacts with |\n"
                    "| **Actions** | Choices the agent can make |\n"
                    "| **Rewards** | Feedback signals (positive or negative) |\n"
                    "| **Policy** | The strategy the agent follows |\n"
                    "| **State** | Current situation of the agent |\n\n"
                    "## How It Works\n"
                    "1. Agent observes the current state\n"
                    "2. Agent takes an action\n"
                    "3. Environment returns new state and reward\n"
                    "4. Agent updates its policy based on reward\n"
                    "5. Repeat until optimal policy is learned\n\n"
                    "## Applications\n"
                    "- 🎮 Game playing (AlphaGo, Atari games)\n"
                    "- 🤖 Robotics and automation\n"
                    "- 🚗 Autonomous vehicles\n"
                    "- 📺 Recommendation systems\n"
                    "- 🏭 Industrial automation\n\n"
                    "## Key Difference\n"
                    "Unlike supervised learning, RL learns through **trial and error** rather than labeled data.\n\n"
                    "Would you like to know more about any specific RL algorithm or application?"
                )
            
            if any(t in topic_lower for t in ["artificial intelligence", "ai", "machine learning", "deep learning"]):
                return (
                    "# 🤖 Artificial Intelligence (AI)\n\n"
                    "## Definition\n"
                    "Artificial Intelligence (AI) is the simulation of human intelligence by machines, "
                    "enabling them to perform tasks that typically require human intelligence.\n\n"
                    "## Key Branches\n"
                    "| Branch | Description |\n"
                    "|--------|-------------|\n"
                    "| **Machine Learning** | Systems that learn from data |\n"
                    "| **Deep Learning** | Neural networks with multiple layers |\n"
                    "| **Natural Language Processing** | Understanding human language |\n"
                    "| **Computer Vision** | Interpreting visual information |\n"
                    "| **Robotics** | Physical agents interacting with the world |\n"
                    "| **Expert Systems** | Rule-based decision making |\n\n"
                    "## Applications\n"
                    "- 🗣️ Virtual assistants (Siri, Alexa, Mitra)\n"
                    "- 🖼️ Image and speech recognition\n"
                    "- 🚗 Autonomous vehicles\n"
                    "- 🏥 Medical diagnosis\n"
                    "- 💰 Financial trading\n"
                    "- 🎮 Game playing (Chess, Go)\n\n"
                    "## Impact\n"
                    "AI is transforming industries and creating new possibilities, while also raising "
                    "important ethical considerations about privacy, bias, and job displacement.\n\n"
                    "Would you like me to elaborate on any specific branch or application?"
                )
            
            if any(t in topic_lower for t in ["python", "programming", "coding"]):
                return (
                    "# 🐍 Python Programming Language\n\n"
                    "## Overview\n"
                    "Python is a popular, versatile programming language known for its readability and simplicity. "
                    "It's one of the most widely-used languages in the world.\n\n"
                    "## Key Features\n"
                    "- ✅ Easy to learn and read\n"
                    "- ✅ Large standard library\n"
                    "- ✅ Cross-platform compatibility\n"
                    "- ✅ Strong community support\n"
                    "- ✅ Multiple programming paradigms\n\n"
                    "## Use Cases\n"
                    "| Domain | Applications |\n"
                    "|--------|-------------|\n"
                    "| **Data Science** | NumPy, Pandas, Matplotlib |\n"
                    "| **Machine Learning** | TensorFlow, PyTorch, Scikit-learn |\n"
                    "| **Web Development** | Django, Flask, FastAPI |\n"
                    "| **Automation** | Scripting, task automation |\n"
                    "| **Scientific Computing** | SciPy, SymPy |\n\n"
                    "## Popular Libraries\n"
                    "- 📊 **Data Analysis**: Pandas, NumPy\n"
                    "- 🤖 **AI/ML**: TensorFlow, PyTorch\n"
                    "- 🌐 **Web**: Django, Flask\n"
                    "- 📈 **Visualization**: Matplotlib, Seaborn\n\n"
                    "Would you like to learn about a specific Python topic or library?"
                )
            
            if any(t in topic_lower for t in ["api", "application programming interface"]):
                return (
                    "# 🔌 API (Application Programming Interface)\n\n"
                    "## Definition\n"
                    "An API is a set of rules that allows different software applications to communicate "
                    "with each other. It defines the methods and data formats for requesting and receiving information.\n\n"
                    "## Types of APIs\n"
                    "| Type | Description | Use Case |\n"
                    "|------|-------------|----------|\n"
                    "| **REST** | Uses HTTP methods (GET, POST, PUT, DELETE) | Web services |\n"
                    "| **GraphQL** | Query language for APIs | Complex data requirements |\n"
                    "| **WebSocket** | Real-time bidirectional communication | Chat, live updates |\n"
                    "| **gRPC** | High-performance RPC framework | Microservices |\n\n"
                    "## HTTP Methods\n"
                    "- **GET**: Retrieve data\n"
                    "- **POST**: Create new resource\n"
                    "- **PUT**: Update existing resource\n"
                    "- **DELETE**: Remove resource\n\n"
                    "## Example (REST)\n"
                    "```http\n"
                    "GET /api/users/123\n"
                    "Authorization: Bearer token\n"
                    "```\n\n"
                    "## Why APIs Matter\n"
                    "- 🔗 Enable software integration\n"
                    "- 📱 Power mobile and web apps\n"
                    "- ☁️ Connect cloud services\n"
                    "- 🤖 Enable AI/ML model deployment\n\n"
                    "Would you like to learn about implementing or using a specific type of API?"
                )
            
            # Space/Astronomy topics
            if any(t in topic_lower for t in ["moon", "luna", "lunar"]):
                return (
                    "# 🌙 The Moon\n\n"
                    "## Overview\n"
                    "The Moon is Earth's only natural satellite, orbiting at an average distance of 384,400 km. "
                    "It's the fifth largest satellite in the Solar System.\n\n"
                    "## Key Facts\n"
                    "| Property | Value |\n"
                    "|----------|-------|\n"
                    "| **Diameter** | 3,474 km |\n"
                    "| **Distance from Earth** | 384,400 km (average) |\n"
                    "| **Orbital Period** | 27.3 days |\n"
                    "| **Surface Temperature** | -173°C to 127°C |\n"
                    "| **Age** | ~4.5 billion years |\n\n"
                    "## Formation\n"
                    "The Moon formed about 4.5 billion years ago, likely from debris after a Mars-sized object "
                    "collided with early Earth.\n\n"
                    "## Phases\n"
                    "1. 🌑 New Moon\n"
                    "2. 🌒 Waxing Crescent\n"
                    "3. 🌓 First Quarter\n"
                    "4. 🌔 Waxing Gibbous\n"
                    "5. 🌕 Full Moon\n"
                    "6. 🌖 Waning Gibbous\n"
                    "7. 🌗 Last Quarter\n"
                    "8. 🌘 Waning Crescent\n\n"
                    "## Exploration\n"
                    "- 🚀 **Apollo Missions**: 6 successful landings (1969-1972)\n"
                    "- 🇺🇸 **Artemis Program**: NASA's return to the Moon\n"
                    "- 🇨🇳 **Chang'e Missions**: Chinese lunar exploration\n\n"
                    "Would you like to know more about any specific aspect of the Moon?"
                )
            
            if any(t in topic_lower for t in ["sun", "star", "solar"]):
                return (
                    "# ☀️ The Sun\n\n"
                    "## Overview\n"
                    "The Sun is the star at the center of our Solar System. It's a nearly perfect sphere of hot plasma.\n\n"
                    "## Key Facts\n"
                    "| Property | Value |\n"
                    "|----------|-------|\n"
                    "| **Type** | G-type main-sequence star |\n"
                    "| **Diameter** | 1,391,000 km |\n"
                    "| **Surface Temperature** | 5,500°C |\n"
                    "| **Core Temperature** | 15,000,000°C |\n"
                    "| **Age** | ~4.6 billion years |\n\n"
                    "## Structure\n"
                    "- **Core**: Nuclear fusion occurs here\n"
                    "- **Radiative Zone**: Energy moves outward\n"
                    "- **Convective Zone**: Hot plasma rises\n"
                    "- **Photosphere**: Visible surface\n"
                    "- **Chromosphere**: Inner atmosphere\n"
                    "- **Corona**: Outer atmosphere\n\n"
                    "Would you like to learn more about the Sun?"
                )
            
            if any(t in topic_lower for t in ["earth", "planet", "world"]):
                return (
                    "# 🌍 Earth\n\n"
                    "## Overview\n"
                    "Earth is the third planet from the Sun and the only known planet to harbor life.\n\n"
                    "## Key Facts\n"
                    "| Property | Value |\n"
                    "|----------|-------|\n"
                    "| **Diameter** | 12,742 km |\n"
                    "| **Distance from Sun** | 149.6 million km |\n"
                    "| **Orbital Period** | 365.25 days |\n"
                    "| **Rotation Period** | 24 hours |\n"
                    "| **Age** | ~4.5 billion years |\n"
                    "| **Water Coverage** | 71% |\n\n"
                    "## Structure\n"
                    "- **Core**: Inner and outer core (iron/nickel)\n"
                    "- **Mantle**: Semi-solid rock\n"
                    "- **Crust**: Thin outer layer\n"
                    "- **Atmosphere**: Nitrogen, Oxygen, etc.\n\n"
                    "## Life Support\n"
                    "- 🌡️ Suitable temperature range\n"
                    "- 💧 Liquid water\n"
                    "- 🛡️ Magnetic field (protection from solar wind)\n"
                    "- 🌬️ Atmosphere (oxygen for breathing)\n\n"
                    "Would you like to know more about Earth?"
                )
            
            # Generic knowledge response
            return (
                f"Regarding '{topic}': This is a great question! While I don't have real-time internet access "
                f"to provide the latest information, I can share what I know. "
                f"Could you tell me more about what specific aspect of {topic} you'd like to know?"
            )
        
        return "I'd be happy to help explain that. Could you be more specific about what you'd like to know?"

    # ===== WHY / HOW QUESTIONS =====
    # Only trigger for very specific patterns, not "explain me about X"
    if any(token in lower for token in ["why", "how does", "how do"]):
        return (
            "That's an interesting question! Let me provide some context:\n\n"
            "While I don't have real-time internet access for the latest information, I can help explain "
            "concepts based on my training data. Could you be more specific about what aspect you'd like me to focus on?"
        )

    # ===== WEATHER =====
    if "weather" in lower:
        if location:
            return f"I can help with weather, but I need live weather data to check conditions for {location}. Please check a weather service for current conditions."
        return "I can help with weather, but I need the city or location you want me to check. Please provide a location for weather information."

    # ===== THANKS =====
    if any(token in lower for token in ["thank you", "thanks", "thx", "appreciate"]):
        return "You're welcome! Is there anything else I can help you with?"

    # ===== FAREWELL =====
    if any(token in lower for token in ["bye", "goodbye", "see you", "farewell", "take care"]):
        return "Goodbye! Feel free to come back anytime you need assistance. Have a great day!"

    # ===== YES/NO =====
    if lower in ["yes", "yeah", "yep", "sure", "ok", "okay"]:
        return "Great! What would you like me to do next?"
    if lower in ["no", "nope", "nah", "nothing"]:
        return "Alright! Let me know if you need anything."

    # ===== MESSAGING =====
    if any(token in lower for token in ["send email", "send an email", "email someone"]):
        return "I can send emails for you. Please provide:\n1. Recipient email address\n2. Subject\n3. Message content"
    if "whatsapp" in lower:
        return "I can send WhatsApp messages. Please provide the recipient's phone number and your message."
    if "telegram" in lower:
        return "I can send Telegram messages. Please provide the username or chat ID and your message."
    if "instagram" in lower:
        return "I can help with Instagram messaging. Please provide the recipient and your message."

    # ===== TASKS =====
    if "ems" in lower or "assign task" in lower:
        return "I can create that EMS task. Please provide:\n1. Task title\n2. Assignee\n3. Priority (high/medium/low)"
    if "create task" in lower or lower.startswith("task ") or " new task" in lower:
        return "I can create that task. Please provide the task title and any details or deadline."

    # ===== CALENDAR =====
    if any(token in lower for token in ["calendar", "meeting", "schedule", "appointment", "event"]):
        return "I can help with calendar events. Please provide:\n1. Event title\n2. Date\n3. Time\n4. Any other details"

    # ===== REMINDERS =====
    if "reminder" in lower or "remind me" in lower or "alert me" in lower:
        return "I can set that reminder. Please tell me:\n1. What to remind you about\n2. When it should trigger"

    # ===== QUESTIONS ABOUT SELF =====
    if any(token in lower for token in ["are you", "can you", "do you"]):
        if "real" in lower or "human" in lower or "person" in lower:
            return "I'm an AI assistant called Mitra. I'm not human, but I'm designed to help you with various tasks efficiently."
        if "know" in lower or "understand" in lower:
            return "I have knowledge from my training data and can help with many topics. I can also perform actions like sending messages, setting reminders, and managing tasks."

    # ===== DEFAULT RESPONSE =====
    return (
        f"I understand you're asking about '{text[:50]}...' "
        f"Let me help you with that. Could you provide a bit more detail about what specific aspect "
        f"you'd like me to address?"
    )


def _looks_unusable(response: str, query: str) -> bool:
    if not response or not response.strip():
        return True

    cleaned = response.strip()
    lowered = cleaned.lower()
    query_text = _normalized_text(query).lower()

    # Only flag old-style mock responses, not knowledge base responses
    if lowered.startswith("[uniguru mock]") or lowered.startswith("[groq mock]") or lowered.startswith("[chatgpt mock]"):
        return True
    if "mock" in lowered and "response to" in lowered:
        return True
    if lowered.startswith("context:"):
        return True
    if cleaned == query or lowered == query_text:
        return True
    return False


async def generate_generic_response(
    query: str,
    context: Dict[str, Any] | None = None,
    model: str | None = None,
) -> str:
    import re
    
    # ===== CHECK FOR SIMPLE MATH FIRST (before LLM) =====
    text = query.strip()
    lower = text.lower()
    
    # Convert word operators to symbols
    def convert_word_operators(t):
        t = re.sub(r'\bplus\b', '+', t)
        t = re.sub(r'\bminus\b', '-', t)
        t = re.sub(r'\btimes\b', '*', t)
        t = re.sub(r'\bmultiplied by\b', '*', t)
        t = re.sub(r'\bdivided by\b', '/', t)
        t = re.sub(r'\bover\b', '/', t)
        t = re.sub(r'\bmod\b', '%', t)
        t = re.sub(r'\bmodulo\b', '%', t)
        return t
    
    def safe_eval(expr):
        cleaned = re.sub(r'[^0-9\+\-\*\/\%\.\(\)\s]', '', expr)
        if not cleaned:
            return None
        try:
            result = eval(cleaned, {"__builtins__": {}}, {})
            return result
        except:
            return None
    
    # Convert word operators
    converted_text = convert_word_operators(lower)
    
    # Check for simple math expressions (just numbers and operators, no words)
    # This catches: 2+2, 10*5, (3+4)*2, etc.
    simple_math_pattern = re.match(r'^[\d\s\+\-\*\/\%\.\(\)]+$', converted_text.strip())
    
    # Check for "what is/what's" followed by pure math
    what_is_math = re.match(r'^(?:what is|what\'s|calculate|compute|solve|evaluate)\s+([\d\s\+\-\*\/\%\.\(\)]+)$', converted_text.strip())
    
    if simple_math_pattern or what_is_math:
        expr = None
        if what_is_math:
            expr = what_is_math.group(1).strip()
        elif simple_math_pattern:
            expr = converted_text.strip()
        
        if expr:
            result = safe_eval(expr)
            if result is not None:
                if isinstance(result, float) and result == int(result):
                    result = int(result)
                return (
                    f"# 🧮 Calculation Result\n\n"
                    f"**Expression:** `{expr}`\n\n"
                    f"**Answer:** `{result}`\n\n"
                    f"Need help with another calculation?"
                )
    
    # ===== CHECK FOR GREETINGS & COMMON QUERIES (before LLM) =====
    # Only match greetings at the START of the query, not as substrings
    greeting_tokens = ["how are you", "how're you", "how do you do",
                       "hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    identity_tokens = ["what is your name", "what's your name", "who are you", "tell me about yourself"]
    capability_tokens = ["what can you do", "help me with", "how can you help",
                         "what are your features", "capabilities"]

    all_quick_tokens = greeting_tokens + identity_tokens + capability_tokens
    if any(lower.startswith(token) or lower == token for token in all_quick_tokens):
        return build_fallback_response(query, context)

    # ===== LET LLM HANDLE EVERYTHING ELSE =====
    # The LLM is capable of answering ANY question - let it do its job
    prompt = build_response_prompt(query, context)
    selected_model = _preferred_model(model)

    try:
        response = await llm_bridge.call_llm(selected_model, prompt)
        if _looks_unusable(response, query):
            return build_fallback_response(query, context)
        return _normalized_text(response)
    except Exception:
        return build_fallback_response(query, context)
