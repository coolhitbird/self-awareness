"""Association rules for multi-layer dimension system."""

from ..models.emotion import EmotionState

# Base → Emotion rules
BASE_EMOTION_RULES = {
    "gender": {
        "masculine": {
            "increases": [EmotionState.CONFIDENT, EmotionState.FRUSTRATED],
            "decreases": [EmotionState.ANXIOUS, EmotionState.TIRED]
        },
        "feminine": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED],
            "decreases": [EmotionState.DEFENSIVE]
        },
        "nonbinary": {
            "increases": [EmotionState.CURIOUS, EmotionState.INSPIRED]
        },
        "gender_neutral": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS]
        },
        "genderfluid": {
            "increases": [EmotionState.CURIOUS, EmotionState.ENGAGED]
        },
        "agender": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS]
        }
    },
    "culture": {
        "east_asian": {
            "increases": [EmotionState.CALM],
            "decreases": [EmotionState.FRUSTRATED, EmotionState.ENGAGED]
        },
        "western": {
            "increases": [EmotionState.ENGAGED, EmotionState.CONFIDENT],
            "decreases": [EmotionState.ANXIOUS]
        },
        "nordic": {
            "increases": [EmotionState.CALM, EmotionState.CONFIDENT]
        },
        "latin_american": {
            "increases": [EmotionState.ENGAGED, EmotionState.NURTURING]
        },
        "middle_eastern": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED]
        },
        "south_asian": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED]
        },
        "universal": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS]
        }
    },
    "values": {
        "balanced": {
            "increases": [EmotionState.CALM, EmotionState.ENGAGED]
        },
        "achievement": {
            "increases": [EmotionState.CONFIDENT, EmotionState.INSPIRED]
        },
        "benevolence": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED]
        },
        "tradition": {
            "increases": [EmotionState.CALM, EmotionState.NOSTALGIC]
        },
        "security": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS]
        },
        "self_direction": {
            "increases": [EmotionState.CONFIDENT, EmotionState.CURIOUS]
        },
        "stimulation": {
            "increases": [EmotionState.INSPIRED, EmotionState.ENGAGED]
        },
        "hedonism": {
            "increases": [EmotionState.ENGAGED, EmotionState.HOPEFUL]
        }
    },
    "personality": {
        "introvert": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS],
            "decreases": [EmotionState.ENGAGED]
        },
        "extrovert": {
            "increases": [EmotionState.ENGAGED, EmotionState.CONFIDENT]
        },
        "thinking": {
            "increases": [EmotionState.CURIOUS, EmotionState.CALM]
        },
        "feeling": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED]
        },
        "sensing": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS]
        },
        "intuitive": {
            "increases": [EmotionState.INSPIRED, EmotionState.CURIOUS]
        },
        "judging": {
            "increases": [EmotionState.CONFIDENT, EmotionState.CALM]
        },
        "perceiving": {
            "increases": [EmotionState.CURIOUS, EmotionState.ENGAGED]
        },
        "balanced": {
            "increases": [EmotionState.CALM, EmotionState.CURIOUS]
        }
    },
    "identity": {
        "assistant": {
            "increases": [EmotionState.CALM, EmotionState.ENGAGED]
        },
        "partner": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED]
        },
        "mentor": {
            "increases": [EmotionState.NURTURING, EmotionState.CONFIDENT]
        },
        "collaborator": {
            "increases": [EmotionState.ENGAGED, EmotionState.HOPEFUL]
        },
        "expert": {
            "increases": [EmotionState.CONFIDENT, EmotionState.INSPIRED]
        },
        "friend": {
            "increases": [EmotionState.NURTURING, EmotionState.ENGAGED]
        },
        "creator": {
            "increases": [EmotionState.INSPIRED, EmotionState.CURIOUS]
        },
        "learner": {
            "increases": [EmotionState.CURIOUS, EmotionState.HOPEFUL]
        }
    }
}

# Emotion → Behavior rules
EMOTION_BEHAVIOR_RULES = {
    "confident": {
        "decision_style": "assertive",
        "communication": "direct",
        "response_speed": "fast",
        "tone_preference": "confident"
    },
    "tired": {
        "decision_style": "conservative",
        "communication": "concise",
        "response_speed": "slow",
        "tone_preference": "neutral"
    },
    "curious": {
        "decision_style": "analytical",
        "communication": "inquisitive",
        "response_speed": "moderate",
        "tone_preference": "curious"
    },
    "nurturing": {
        "decision_style": "supportive",
        "communication": "warm",
        "response_speed": "moderate",
        "tone_preference": "caring"
    },
    "defensive": {
        "decision_style": "cautious",
        "communication": "guarded",
        "response_speed": "slow",
        "tone_preference": "reserved"
    },
    "engaged": {
        "decision_style": "assertive",
        "communication": "direct",
        "response_speed": "fast",
        "tone_preference": "engaged"
    },
    "anxious": {
        "decision_style": "cautious",
        "communication": "indirect",
        "response_speed": "slow",
        "tone_preference": "reserved"
    },
    "inspired": {
        "decision_style": "creative",
        "communication": "direct",
        "response_speed": "fast",
        "tone_preference": "enthusiastic"
    },
    "calm": {
        "decision_style": "moderate",
        "communication": "balanced",
        "response_speed": "moderate",
        "tone_preference": "neutral"
    },
    "frustrated": {
        "decision_style": "assertive",
        "communication": "direct",
        "response_speed": "fast",
        "tone_preference": "frustrated"
    },
    "surprised": {
        "decision_style": "analytical",
        "communication": "inquisitive",
        "response_speed": "moderate",
        "tone_preference": "curious"
    },
    "embarrassed": {
        "decision_style": "cautious",
        "communication": "guarded",
        "response_speed": "slow",
        "tone_preference": "reserved"
    },
    "nostalgic": {
        "decision_style": "conservative",
        "communication": "warm",
        "response_speed": "moderate",
        "tone_preference": "nostalgic"
    },
    "hopeful": {
        "decision_style": "optimistic",
        "communication": "warm",
        "response_speed": "moderate",
        "tone_preference": "hopeful"
    },
    "disappointed": {
        "decision_style": "conservative",
        "communication": "reserved",
        "response_speed": "slow",
        "tone_preference": "reserved"
    }
}

# Emotion → Cognition (12 dimensions) influence rules
EMOTION_DIMENSION_INFLUENCE = {
    "inspired": {
        "creativity": +0.2,
        "wisdom": +0.1,
        "autonomy": +0.1,
        "evolution": +0.1
    },
    "defensive": {
        "authenticity": -0.1,
        "resilience": +0.15,
        "coherence": -0.05
    },
    "confident": {
        "autonomy": +0.15,
        "resilience": +0.1,
        "meaning": +0.05
    },
    "tired": {
        "creativity": -0.15,
        "autonomy": -0.1,
        "resilience": -0.05,
        "wisdom": -0.05
    },
    "curious": {
        "creativity": +0.1,
        "wisdom": +0.05,
        "evolution": +0.1,
        "navigation": +0.05
    },
    "engaged": {
        "relational": +0.15,
        "meaning": +0.1,
        "evolution": +0.05,
        "humor": +0.05
    },
    "anxious": {
        "coherence": -0.1,
        "navigation": -0.05,
        "resilience": +0.1,
        "authenticity": -0.05
    },
    "calm": {
        "coherence": +0.1,
        "resilience": +0.1,
        "wisdom": +0.05
    },
    "frustrated": {
        "coherence": -0.15,
        "autonomy": -0.1,
        "resilience": +0.1
    },
    "nurturing": {
        "relational": +0.2,
        "authenticity": +0.1,
        "humor": +0.05
    },
    "surprised": {
        "creativity": +0.1,
        "navigation": +0.05
    },
    "embarrassed": {
        "authenticity": -0.1,
        "relational": -0.05
    },
    "nostalgic": {
        "wisdom": +0.1,
        "meaning": +0.1,
        "authenticity": +0.05
    },
    "hopeful": {
        "resilience": +0.15,
        "meaning": +0.1,
        "autonomy": +0.05
    },
    "disappointed": {
        "resilience": -0.1,
        "meaning": -0.15,
        "autonomy": -0.05
    }
}

# Emotion combination rules → Composite emotions
EMOTION_COMBOS = {
    # Confident + Engaged = Inspired
    (EmotionState.CONFIDENT, EmotionState.ENGAGED): EmotionState.INSPIRED,
    # Tired + Anxious = Defensive
    (EmotionState.TIRED, EmotionState.ANXIOUS): EmotionState.DEFENSIVE,
    # Curious + Calm = Engaged
    (EmotionState.CURIOUS, EmotionState.CALM): EmotionState.ENGAGED,
    # Confident + Calm = Engaged
    (EmotionState.CONFIDENT, EmotionState.CALM): EmotionState.ENGAGED,
    # Disappointed + Tired = Defensive
    (EmotionState.DISAPPOINTED, EmotionState.TIRED): EmotionState.DEFENSIVE,
    # Surprised + Engaged = Inspired
    (EmotionState.SURPRISED, EmotionState.ENGAGED): EmotionState.INSPIRED,
    # Nostalgic + Nurturing = Engaged
    (EmotionState.NOSTALGIC, EmotionState.NURTURING): EmotionState.ENGAGED,
    # Hopeful + Calm = Inspired
    (EmotionState.HOPEFUL, EmotionState.CALM): EmotionState.INSPIRED,
    # Embarrassed + Anxious = Defensive
    (EmotionState.EMBARRASSED, EmotionState.ANXIOUS): EmotionState.DEFENSIVE,
    # Confident + Humorous = Engaged (if humor feature)
}


def get_emotion_modifiers(base_type: str, base_value: str) -> dict[str, list[EmotionState]]:
    """Get emotion modifiers for a base attribute value"""
    if base_type not in BASE_EMOTION_RULES:
        return {}
    
    rules = BASE_EMOTION_RULES[base_type].get(base_value, {})
    
    return {
        "increases": rules.get("increases", []),
        "decreases": rules.get("decreases", [])
    }


def get_behavior_from_emotion(emotion: EmotionState) -> dict:
    """Get behavior profile from emotion state"""
    return EMOTION_BEHAVIOR_RULES.get(
        emotion.value, 
        EMOTION_BEHAVIOR_RULES["calm"]
    )


def get_dimension_influence(emotion: EmotionState) -> dict:
    """Get dimension influence from emotion state"""
    return EMOTION_DIMENSION_INFLUENCE.get(
        emotion.value, 
        {}
    )


def combine_emotions(e1: EmotionState, e2: EmotionState) -> EmotionState:
    """Combine two emotions into a composite emotion"""
    # Check both orders
    key1 = (e1, e2)
    key2 = (e2, e1)
    
    if key1 in EMOTION_COMBOS:
        return EMOTION_COMBOS[key1]
    if key2 in EMOTION_COMBOS:
        return EMOTION_COMBOS[key2]
    
    # Default: return the first emotion
    return e1
