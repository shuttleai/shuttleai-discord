class Conversation:
    def __init__(self, max_memory=8):
        self.messages = []
        self.max_memory = max_memory

    def add_message(self, role: str, content: str):
        if len(self.messages) >= self.max_memory:
            self.messages.pop(0)  
        self.messages.append({'role': role, 'content': content})

    def get_messages(self):
        return self.messages
    
    def get_messages_by_role(self, role: str):
        return [message for message in self.messages if message['role'] == role]
    
    def get_last_message(self):
        return self.messages[-1] if len(self.messages) > 0 else None
    
class ConversationManager:
    def __init__(self):
        self.conversations = {}

    def add_message(self, discord_id: str, role: str, content: str):
        if discord_id not in self.conversations:
            self.conversations[discord_id] = Conversation()
        self.conversations[discord_id].add_message(role, content)

    def get_messages(self, discord_id: str):
        return self.conversations[discord_id].get_messages() if discord_id in self.conversations else None
    
    def clear_messages(self, discord_id: str):
        if discord_id in self.conversations:
            self.conversations[discord_id] = Conversation()

    def get_or_create_conversation(self, discord_id: str):
        if discord_id not in self.conversations:
            self.conversations[discord_id] = Conversation()
        return self.conversations[discord_id]


conversation_manager = ConversationManager()