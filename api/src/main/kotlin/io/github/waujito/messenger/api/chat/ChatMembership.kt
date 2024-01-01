package io.github.waujito.messenger.api.chat

import jakarta.persistence.*
import org.hibernate.annotations.OnDelete
import org.hibernate.annotations.OnDeleteAction
import org.springframework.data.annotation.CreatedDate
import org.springframework.data.jpa.domain.AbstractPersistable
import org.springframework.data.jpa.domain.support.AuditingEntityListener
import java.util.*

/**
 * Represents relation between user and chat
 */
@Entity
@EntityListeners(AuditingEntityListener::class)
class ChatMembership(userId: String, chat: Chat) : AbstractPersistable<UUID>() {

    @Column(nullable = false, updatable = false)
    var userId: String = userId
        private set

    @ManyToOne(optional = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    var chat: Chat = chat
        private set

    @CreatedDate
    @Column(nullable = false, updatable = false)
    var joinedAt: Date? = null
        private set

    override fun equals(other: Any?): Boolean {
        if (super.equals(other)) return true

        if (other is ChatMembership){
            return other.userId == this.userId && other.chat == this.chat
        }

        return false
    }

    override fun hashCode(): Int {
        var result = super.hashCode()
        result = 31 * result + userId.hashCode()
        result = 31 * result + chat.hashCode()
        result = 31 * result + (joinedAt?.hashCode() ?: 0)
        return result
    }
}