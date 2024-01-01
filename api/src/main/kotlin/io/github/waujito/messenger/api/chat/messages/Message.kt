package io.github.waujito.messenger.api.chat.messages

import io.github.waujito.messenger.api.chat.Chat
import jakarta.persistence.*
import jakarta.validation.constraints.Size
import org.hibernate.annotations.*
import org.springframework.data.annotation.CreatedDate
import org.springframework.data.annotation.LastModifiedDate
import org.springframework.data.jpa.domain.AbstractPersistable
import org.springframework.data.jpa.domain.support.AuditingEntityListener
import java.util.Date
import java.util.UUID

@Entity
@EntityListeners(AuditingEntityListener::class)
class Message(chat: Chat, authorId: String, content: String) : AbstractPersistable<UUID>() {
    @ManyToOne(optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    var chat: Chat = chat
        private set

    @Column(nullable = false, updatable = false)
    var authorId: String = authorId
        private set

    @Column(columnDefinition = "TEXT", nullable = false, updatable = true)
    @Size(max=8192)
    var content: String = content
        private set

    @CreatedDate
    @Column(nullable = false, updatable = false)
    var createdAt: Date? = null
        private set

    @LastModifiedDate
    @Column(nullable = true, updatable = true)
    var updatedAt: Date? = null
        private set

    override fun equals(other: Any?): Boolean {
        return super.equals(other)
    }

    override fun hashCode(): Int {
        var result = super.hashCode()
        result = 31 * result + chat.hashCode()
        result = 31 * result + authorId.hashCode()
        result = 31 * result + content.hashCode()
        result = 31 * result + (createdAt?.hashCode() ?: 0)
        result = 31 * result + (updatedAt?.hashCode() ?: 0)
        return result
    }
}