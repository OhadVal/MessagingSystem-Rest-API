from flasgger import swag_from
from flask import Blueprint, jsonify, request

from API.User.user_api import token_required
from database import db
from models.message import Message, messages_schema, message_schema
from models.user import User

message_blueprint = Blueprint('message_api', __name__)


@message_blueprint.route('/messages')
@token_required
@swag_from('all_messages_for_user.yaml')
def get_all_messages_for_user(current_user: User):
    """
    Gets all messages in DB for the logged in user
    Returns: JSON Object
    """
    all_messages_for_user = Message.query.filter(
        (Message.sender == current_user.username) | (Message.receiver == current_user.username)
    ).get_or_404(description='No Messages for this user')
    return jsonify(messages_schema.dump(all_messages_for_user))


@message_blueprint.route('/unread_messages')
@token_required
@swag_from('all_unread_messages_for_user.yaml')
def get_all_unread_messages_for_user(current_user: User):
    """
    Gets all unread messages in DB for the logged in user
    Returns: JSON Object
    """
    unread_messages = Message.query.filter_by(receiver=current_user.username, read_by_receiver=False)
    return jsonify(messages_schema.dump(unread_messages))


@message_blueprint.route('/read_message/<int:message_id>')
@token_required
@swag_from('read_message.yaml')
def read_message(current_user: User, message_id: int):
    """
    Reads a message, only if the user is the receiver or sender
    Args:
        current_user: logged in user
        message_id: message to read

    Returns: JSON (message or error)
    """
    message = Message.query.filter_by(id=message_id).first_or_404(description='No message with this id')
    if message.receiver == current_user.username:
        # Only receiver can mark the message as read
        message.read_by_receiver = True
        db.session.commit()
        return message_schema.dump(message)
    return jsonify({'error': 'User is unauthorized to read this message'}), 403


@message_blueprint.route('/delete_message/<int:message_id>', methods=['DELETE'])
@token_required
@swag_from('delete_message.yaml')
def delete_message(current_user: User, message_id: int):
    message = Message.query.filter_by(id=message_id).first_or_404(description='No message with this id')
    # Only if receiver can mark the message as read
    if message.receiver == current_user.username or message.sender == current_user.username:
        db.session.delete(message)
        db.session.commit()
        return message_schema.dump(message)
    return jsonify({'error': 'User is unauthorized to read this message'}), 403


@message_blueprint.route('/message', methods=['POST'])
@token_required
@swag_from('new_message.yaml')
def create_message(current_user: User):
    data = request.get_json(force=True)
    try:
        # Check if receiver exist in DB
        receiver = User.query \
            .filter_by(username=data['receiver']) \
            .first_or_404(description="No receiver with that name")

        # Create new message
        new_message = Message(
            sender=current_user.username,
            receiver=data['receiver'],
            message=data['message'],
            subject=data['subject']
        )

        # Insert to DB
        db.session.add(new_message)
        db.session.commit()
        return message_schema.dump(new_message)
    except KeyError as e:
        return jsonify({'error': 'Missing values in request'}), 400
