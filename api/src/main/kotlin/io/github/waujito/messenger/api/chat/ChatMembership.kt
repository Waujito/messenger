package io.github.waujito.messenger.api.chat

import jakarta.persistence.*
import org.hibernate.annotations.OnDelete
import org.hibernate.annotations.OnDeleteAction
import org.springframework.data.annotation.CreatedDate
import java.util.*

/**
 * Represents relation between user and chat
 */
@Entity
class ChatMembership(userId: String, chat: Chat) {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    var Id: UUID? = null
        private set

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
}