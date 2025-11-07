from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from enum import Enum


class MessageRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """A single chat message."""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    role: MessageRole
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Request for chat conversation."""
    user_id: str
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class GeneratedMaterial(BaseModel):
    """Generated material from chat."""
    material_type: str  # "flyer", "poster", "email", etc.
    title: str
    content: str
    format_instructions: Optional[str] = None


class ChatResponse(BaseModel):
    """Response from chat AI."""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    conversation_id: str
    message: ChatMessage
    generated_materials: Optional[List[GeneratedMaterial]] = None
    suggestions: Optional[List[str]] = None
    timestamp: datetime


class ConversationHistory(BaseModel):
    """Chat conversation history."""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    conversation_id: str
    user_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime