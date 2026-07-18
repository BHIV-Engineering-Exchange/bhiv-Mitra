"""
IntentFlow Module - Seeya's NLU Intent Classification Engine
Provides clean intent classification with entity resolution and smart context.
"""

import re
from typing import Dict, List, Any
from datetime import datetime, timedelta
import dateutil.parser as parser

class IntentFlow:
    def __init__(self):
        # Intent patterns and keywords
        # NOTE: Task-related patterns should only match EXPLICIT task creation requests
        # NOT general questions that happen to contain words like "task" or "create"
        self.intent_patterns = {
            'summarize': ['summarize', 'summary', 'summarise', 'tl;dr', 'key points', 'brief'],
            'task': ['create a task', 'add a task', 'make a task', 'new task for', 'assign task to', 'create todo', 'add to my todo'],
            'search': ['search for', 'find me', 'lookup', 'research about', 'look up'],
            'email': ['send email', 'send an email', 'email to', 'compose email', 'send mail to'],
            'calendar': ['add to calendar', 'schedule meeting', 'create event', 'set appointment', 'add meeting'],
            'reminder': ['set reminder', 'remind me to', 'create reminder', 'add reminder', 'alert me to'],
            'telegram': ['send telegram', 'telegram message to'],
            'instagram': ['send instagram', 'instagram message to', 'send dm on instagram'],
            'ems': ['create ems task', 'assign ems task', 'ems assignment'],
            'device': ['send command to device', 'control device', 'device command'],
            'general': []  # fallback
        }

        # Entity patterns
        self.entity_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'time': r'\b\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\b',
            'duration': r'\b\d+\s*(?:hour|minute|day|week|month)s?\b'
        }

    def classify_intent(self, text: str) -> str:
        """Classify the primary intent from text."""
        text_lower = text.lower()

        for intent, keywords in self.intent_patterns.items():
            if intent == 'general':
                continue
            if any(keyword in text_lower for keyword in keywords):
                return intent

        return 'general'  # fallback

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract and resolve entities from text."""
        entities = {}
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = list(set(matches))

        return entities

    def resolve_dates_times(self, text: str) -> Dict[str, Any]:
        """Resolve date/time references to structured format."""
        resolved = {}

        # Try to parse dates
        try:
            # Look for relative dates
            relative_patterns = {
                'today': datetime.now(),
                'tomorrow': datetime.now() + timedelta(days=1),
                'yesterday': datetime.now() - timedelta(days=1),
                'next week': datetime.now() + timedelta(weeks=1),
                'next month': datetime.now() + timedelta(days=30)
            }

            text_lower = text.lower()
            for rel, date_obj in relative_patterns.items():
                if rel in text_lower:
                    resolved['relative_date'] = rel
                    resolved['resolved_date'] = date_obj.isoformat()
                    break

            # Try to parse absolute dates
            date_matches = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
            if date_matches:
                try:
                    parsed_date = parser.parse(date_matches[0])
                    resolved['absolute_date'] = date_matches[0]
                    resolved['parsed_date'] = parsed_date.isoformat()
                except:
                    pass

        except Exception as e:
            resolved['date_error'] = str(e)

        # Extract times
        time_matches = re.findall(r'\b\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\b', text)
        if time_matches:
            resolved['time'] = time_matches[0]

        return resolved

    def extract_context(self, text: str) -> Dict[str, Any]:
        """Extract smart context from text."""
        context = {
            'urgency': 'normal',
            'priority': 'medium',
            'sentiment': 'neutral'
        }

        text_lower = text.lower()

        # Urgency detection
        urgent_keywords = ['urgent', 'asap', 'immediately', 'emergency', 'critical']
        if any(word in text_lower for word in urgent_keywords):
            context['urgency'] = 'high'

        # Priority detection
        high_priority = ['important', 'priority', 'critical', 'deadline']
        if any(word in text_lower for word in high_priority):
            context['priority'] = 'high'

        # Simple sentiment (could be enhanced with proper NLP)
        positive = ['good', 'great', 'excellent', 'happy', 'thanks']
        negative = ['bad', 'terrible', 'angry', 'frustrated', 'problem']

        if any(word in text_lower for word in positive):
            context['sentiment'] = 'positive'
        elif any(word in text_lower for word in negative):
            context['sentiment'] = 'negative'

        return context

    def process_text(self, text: str) -> Dict[str, Any]:
        """Process text through the complete IntentFlow pipeline."""
        intent = self.classify_intent(text)
        entities = self.extract_entities(text)
        dates_times = self.resolve_dates_times(text)
        context = self.extract_context(text)

        return {
            "intent": intent,
            "entities": entities,
            "dates_times": dates_times,
            "context": context,
            "confidence": 0.8,  # Placeholder confidence score
            "timestamp": datetime.now().isoformat(),
            "version": "intentflow_v1",
            "original_text": text
        }

# Global instance
intent_flow = IntentFlow()