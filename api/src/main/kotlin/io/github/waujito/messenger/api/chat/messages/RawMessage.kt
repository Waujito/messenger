package io.github.waujito.messenger.api.chat.messages

import org.springframework.data.jpa.domain.AbstractPersistable
import java.util.*


class RawMessage(val authorId: String, val content: String, val createdAt: Date?, val updatedAt: Date?) : AbstractPersistable<UUID>() {
    constructor(message: Message) : this(message.authorId, message.content, message.createdAt, message.updatedAt) {
        this.id = message.id
    }
}