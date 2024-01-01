package io.github.waujito.messenger.api.chat.messages

import io.github.waujito.messenger.api.chat.Chat
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.ManyToOne
import jakarta.validation.constraints.Size
import org.hibernate.annotations.*
import org.springframework.data.annotation.CreatedDate
import org.springframework.data.annotation.LastModifiedDate
import java.util.Date
import java.util.UUID

@Entity
class Message(chat: Chat, authorId: String, content: String) {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    var id: UUID? = null
        private set

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
}