from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .services.ai_service import generate_ai_response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def find_similar_question(message):
    keywords = message.split()

    # Only check last 50 chats (fast + relevant)
    chats = ChatMessage.objects.order_by('-created_at')[:50]

    for chat in chats:
        match_count = 0
        stored_words = chat.message.split()

        for word in keywords:
            if word in stored_words:
                match_count += 1

        if len(keywords) > 0 and (match_count / len(keywords)) >= 0.6:
            return chat

    return None


@api_view(['POST'])
def chat_api(request):
    message = request.data.get("message")

    # Normalize FIRST
    if message:
        message = message.strip().lower()

    # Validation
    if not message:
        return Response({
            "success": False,
            "error": "Message cannot be empty"
        }, status=400)

    if len(message) > 300:
        return Response({
            "success": False,
            "error": "Message too long"
        }, status=400)

    # Get IP
    ip = get_client_ip(request)

    # Get session
    session, _ = ChatSession.objects.get_or_create(ip_address=ip)

    # Exact match cache
    existing_chat = ChatMessage.objects.filter(message=message).first()

    # Smart match
    if not existing_chat:
        existing_chat = find_similar_question(message)

    if existing_chat:
        return Response({
            "success": True,
            "response": existing_chat.response,
            "cached": True
        })

    # AI call
    ai_response = generate_ai_response(message)

    if "Error code" in ai_response:
        return Response({
            "success": False,
            "error": "AI service not available. Please try later."
        }, status=500)

    # Save
    ChatMessage.objects.create(
        session=session,
        message=message,
        response=ai_response
    )

    return Response({
        "success": True,
        "response": ai_response
    })