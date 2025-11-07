from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.chat_service import ChatService
from services.auth_service import AuthService
from models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["ai-chat"])
security = HTTPBearer()
chat_service = ChatService()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to get current authenticated user."""
    user_id = AuthService.verify_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTHENTICATION_ERROR",
                "message": "Invalid or expired token",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # Verify user still exists
    user = AuthService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTHENTICATION_ERROR",
                "message": "User not found",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    return user_id


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Send a message to the AI assistant."""
    try:
        # Ensure the request is for the authenticated user
        if request.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AUTHORIZATION_ERROR",
                    "message": "You can only send messages for your own account",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        # Process the chat message
        response = await chat_service.chat(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Chat processing failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/demo", response_model=ChatResponse)
async def demo_chat(message: str):
    """Demo chat without authentication."""
    try:
        request = ChatRequest(
            user_id="demo-user",
            message=message
        )
        
        response = await chat_service.chat(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Demo chat failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Get conversation history."""
    try:
        conversation = chat_service.get_conversation(conversation_id)
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "CONVERSATION_NOT_FOUND",
                    "message": "Conversation not found",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        # Check if user owns this conversation
        if conversation.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AUTHORIZATION_ERROR",
                    "message": "You can only access your own conversations",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        return conversation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Failed to get conversation: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/conversations")
async def get_user_conversations(current_user_id: str = Depends(get_current_user)):
    """Get all conversations for the current user."""
    try:
        conversations = chat_service.get_user_conversations(current_user_id)
        return {"conversations": conversations}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Failed to get conversations: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )