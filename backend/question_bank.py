"""Question bank for different interview topics and difficulty levels"""

QUESTION_BANK = {
    "leadership": {
        "easy": [
            "Tell me about a time you helped a team member who was struggling.",
            "Describe a situation where you had to motivate your team.",
            "Have you ever had to give constructive feedback? How did you approach it?"
        ],
        "medium": [
            "Tell me about a time you led a team through a difficult project.",
            "Describe a situation where you had to influence people without direct authority.",
            "Tell me about a time when your team disagreed with your decision. How did you handle it?"
        ],
        "hard": [
            "Describe a time you had to make an unpopular decision as a leader.",
            "Tell me about your biggest leadership failure and what you learned.",
            "How do you balance being a strong leader with being collaborative?"
        ]
    },
    "algorithms": {
        "easy": [
            "Explain how you would reverse a string.",
            "How would you find if a string is a palindrome?",
            "Describe how a hash table works."
        ],
        "medium": [
            "How would you detect a cycle in a linked list?",
            "Explain how you'd implement a LRU cache.",
            "Walk me through finding the kth largest element in an array."
        ],
        "hard": [
            "Design an algorithm to find the longest palindromic substring.",
            "How would you implement a trie and what are its use cases?",
            "Explain dynamic programming and give an example of when you'd use it."
        ]
    },
    "system_design": {
        "easy": [
            "How would you design a URL shortener?",
            "Explain the difference between SQL and NoSQL databases.",
            "What is load balancing and why is it important?"
        ],
        "medium": [
            "Design a rate limiter for an API.",
            "How would you design a notification system?",
            "Design a file storage system like Dropbox."
        ],
        "hard": [
            "Design Twitter's feed system.",
            "How would you design a distributed cache?",
            "Design a real-time analytics system for a large e-commerce site."
        ]
    },
    "conflict_resolution": {
        "easy": [
            "Tell me about a time you disagreed with a coworker.",
            "How do you handle criticism?",
            "Describe a situation where you had to compromise."
        ],
        "medium": [
            "Tell me about a time you had to work with a difficult team member.",
            "Describe a situation where you had to navigate office politics.",
            "How do you handle it when your idea is rejected?"
        ],
        "hard": [
            "Tell me about the most difficult conflict you've resolved.",
            "Describe a time when you had to choose between two team members' ideas.",
            "How do you handle a situation where upper management makes a decision you disagree with?"
        ]
    },
    "behavioral": {
        "easy": [
            "Why are you interested in this role?",
            "What are your biggest strengths?",
            "Where do you see yourself in 5 years?"
        ],
        "medium": [
            "Tell me about a time you failed and what you learned.",
            "Describe your ideal work environment.",
            "How do you prioritize when you have multiple deadlines?"
        ],
        "hard": [
            "What's the biggest risk you've ever taken?",
            "Tell me about a time you had to adapt to a major change.",
            "Describe a situation where you had to learn something completely new quickly."
        ]
    }
}

def get_question(topic: str, difficulty: str = "medium") -> str:
    """Get a random question for a topic and difficulty"""
    import random
    
    if topic not in QUESTION_BANK:
        topic = "behavioral"
    
    if difficulty not in QUESTION_BANK[topic]:
        difficulty = "medium"
    
    questions = QUESTION_BANK[topic][difficulty]
    return random.choice(questions)

def get_all_topics() -> list:
    """Get list of all available topics"""
    return list(QUESTION_BANK.keys())
