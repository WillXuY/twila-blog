from flask_smorest import Blueprint
from flask.views import MethodView
from application.schemas.chat import ChatRequestSchema, ConversationSchema, MessageSchema
from application.services.chat_service import handle_chat, get_conversations, get_conversation_messages

chat_bp = Blueprint('chat', __name__, description="Chat related operations")


@chat_bp.route('')
class ChatResource(MethodView):

    @chat_bp.arguments(ChatRequestSchema)
    @chat_bp.response(200)
    def post(self, json_data):
        user_id = json_data['user_id']
        conv_id = json_data.get('conversation_id')
        user_message = json_data['message'].strip()

        return handle_chat(user_id, conv_id, user_message)


@chat_bp.route('/conversations')
class ConversationListResource(MethodView):

    @chat_bp.arguments(ChatRequestSchema(only=['user_id']), location="query")
    @chat_bp.response(200, ConversationSchema(many=True))
    def get(self, args):
        user_id = args['user_id']
        return get_conversations(user_id)


@chat_bp.route('/conversations/<uuid:conversation_id>/messages')
class ConversationMessagesResource(MethodView):

    @chat_bp.arguments(ChatRequestSchema(only=['user_id']), location="query")
    @chat_bp.response(200, MessageSchema(many=True))
    def get(self, args, conversation_id):
        user_id = args['user_id']
        return get_conversation_messages(user_id, conversation_id)
