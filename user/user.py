def register(conn, username):
    if conn.hget('users:', username):
        return None

    user_id = conn.incr('user:id:')

    pipeline = conn.pipeline(True)

    pipeline.hset('users:', username, user_id)

    pipeline.hmset('user:%s' % user_id, {
        'login': username,
        'id': user_id,
        'queue': 0,
        'checking': 0,
        'blocked': 0,
        'sent': 0,
        'delivered': 0
    })
    pipeline.execute()
    return user_id


def sign_in(conn, username) -> int:
    user_id = conn.hget("users:", username)

    if not user_id:
        print("Current user does not exist %s" % username)
        return -1

    conn.sadd("online:", username)
    return int(user_id)


def sign_out(conn, user_id) -> int:
    return conn.srem("online:", conn.hmget("user:%s" % user_id, ["login"])[0])


def create_message(conn, message_text, sender_id, consumer) -> int:
    message_id = int(conn.incr('message:id:'))
    consumer_id = int(conn.hget("users:", consumer))

    if not consumer_id:
        print("Current user does not exist %s, unable to send message" % consumer)
        return

    pipeline = conn.pipeline(True)

    pipeline.hmset('message:%s' % message_id, {
        'text': message_text,
        'id': message_id,
        'sender_id': sender_id,
        'consumer_id': consumer_id,
        'status': "created"
    })
    pipeline.lpush("queue:", message_id)
    pipeline.hmset('message:%s' % message_id, {
        'status': 'queue'
    })
    pipeline.zincrby("sent:", 1, "user:%s" % conn.hmget("user:%s" % sender_id, ["login"])[0])
    pipeline.hincrby("user:%s" % sender_id, "queue", 1)
    pipeline.execute()

    return message_id
