
def send_message_user(vk, user_id, message):
    vk.messages.send(
            random_id = 0,
            user_id=user_id,
            message=message
        )
def send_message_peer(vk, peer_id, message):
    vk.messages.send(
            random_id = 0,
            peer_id=peer_id,
            message=message
        )